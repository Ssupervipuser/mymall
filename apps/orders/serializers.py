from django.utils.datetime_safe import datetime
from rest_framework import serializers
from decimal import Decimal
from django_redis import get_redis_connection
from django.db import transaction


from .models import OrderInfo, OrderGoods
from apps.goods.models import SKU


class CartSKUSerializer(serializers.ModelSerializer):
    """订单中的商品序列化器"""
    count = serializers.IntegerField(label='商品的购买数量')

    class Meta:
        model = SKU
        fields = ['id', 'name', 'default_image_url', 'price', 'count']


class OrderSettlementSerializer(serializers.Serializer):
    """订单序列化器"""
    skus = CartSKUSerializer(many=True)
    freight = serializers.DecimalField(label='运费', max_digits=10, decimal_places=2)




class CommitOrderSerializer(serializers.ModelSerializer):
    """保存订单序列化"""

    class Meta:
        model = OrderInfo
        fields = ['address', 'pay_method', 'order_id']
        read_only_fields = ['order_id']  # 只序列化输出 不做反序列化
        extra_kwargs = {
            'address': {'write_only': True},
            'pay_method': {'write_only': True},
        }

    def create(self, validated_data):
        """在这里 我们同时操作了四张表 订单基本信息表, sku表, spu表 ,订单中商品表 四张表要么一起修改成功,要么都不修改"""
        """保存订单"""
        # 获取当前保存订单时需要的信息

        # 订单编号: 拿当前时间 + 00001  : 20190414154600 + 000000001
        # 获取用户对象
        user = self.context['request'].user
        # 生成订单编号
        order_id = datetime.now().strftime('%Y%m%d%H%M%S') + '%09d' % user.id
        # 获取前端传入的收货地址
        address = validated_data.get('address')
        # 获取前端传入的支付方式
        pay_method = validated_data.get('pay_method')
        # 订单状态
        status = (OrderInfo.ORDER_STATUS_ENUM['UNPAID']
                  if pay_method == OrderInfo.PAY_METHODS_ENUM['ALIPAY']
                  else OrderInfo.ORDER_STATUS_ENUM['UNSEND'])

        with transaction.atomic():  # 手动开启事务

            # 创建事务的保存点
            save_point = transaction.savepoint()
            try:
                # 保存订单基本信息 OrderInfo（一）
                orderInfo = OrderInfo.objects.create(
                    order_id=order_id,
                    user=user,
                    address=address,
                    total_count=0,  # 订单中商品总数量
                    total_amount=Decimal('0.00'),  # 订单总金额
                    freight=Decimal('10.00'),
                    pay_method=pay_method,
                    status=status
                )

                # 从redis读取购物车中被勾选的商品信息
                # 创建redis连接对象
                redis_conn = get_redis_connection('cart')
                # 把redis中hash和set的购物车数据全部获取出来 {sku_id_1: 2}
                cart_dict_redis = redis_conn.hgetall('cart_%d' % user.id)
                selected_ids = redis_conn.smembers('selected_%d' % user.id)

                # 遍历购物车中被勾选的商品信息
                for sku_id_bytes in selected_ids:

                    while True:  # 让用户对同一个商品有无限次下单机会,只到库存真的不足为止
                        # 获取sku对象
                        sku = SKU.objects.get(id=sku_id_bytes)

                        # 获取当前商品的购买数量
                        buy_count = int(cart_dict_redis[sku_id_bytes])
                        # 把当前sku模型中的库存和销量都分别先获取出来
                        origin_sales = sku.sales  # 获取当前要购买商品的原有销量
                        origin_stock = sku.stock  # 获取当前要购买商品的原库存

                        # import time
                        # time.sleep(5)

                        # 判断库存
                        if buy_count > origin_stock:
                            raise serializers.ValidationError('库存不足')

                        # 减少库存，增加销量 SKU
                        # 计算新的库存和销量
                        new_sales = origin_sales + buy_count
                        new_stock = origin_stock - buy_count

                        # sku.sales = new_sales  # 修改sku模型的销量
                        # sku.stock = new_stock  # 修改sku模型的库存
                        # sku.save()
                        # updata更新时会返回 更新数据的条数  0, 1
                        result = SKU.objects.filter(stock=origin_stock, id=sku_id_bytes).update(stock=new_stock, sales=new_sales)
                        if result == 0:  # 如果没有修改成功,说明有抢夺
                            continue


                        # 修改SPU销量
                        spu = sku.goods
                        spu.sales = spu.sales + buy_count
                        spu.save()

                        # 保存订单商品信息 OrderGoods（多）
                        OrderGoods.objects.create(
                            order=orderInfo,
                            sku=sku,
                            count=buy_count,
                            price=sku.price,
                        )

                        # 累加计算总数量和总价 11
                        orderInfo.total_count += buy_count
                        orderInfo.total_amount += (sku.price * buy_count)

                        break  # 当前这个商品下单成功,跳出死循环,进行对下一个商品下单

                # 最后加入邮费和保存订单信息
                orderInfo.total_amount += orderInfo.freight
                orderInfo.save()
            except Exception:
                # 进行暴力回滚
                transaction.savepoint_rollback(save_point)
                raise serializers.ValidationError('库存不足')  # 此行代码不能少 ,不然订单提交失败,前端界面依然正常
            else:
                transaction.savepoint_commit(save_point)  # 如果中间没有出现任何问题,就提交事务



        # 清除购物车中已结算的商品
        pl = redis_conn.pipeline()
        pl.hdel('cart_%d' % user.id, *selected_ids)
        pl.srem('selected_%d' % user.id, *selected_ids)
        pl.execute()

        # 返回订单模型对象
        return orderInfo
