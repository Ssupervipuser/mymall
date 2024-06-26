import base64, pickle
from django_redis import get_redis_connection


def merge_cart_cookie_to_redis(request, user, response):
    """
    登录时合并购物车
    :param request: 登录时借用过来的请求对象
    :param user: 登录时借用过来的用户对象
    :param response: 借用过来准备做删除cookie的响应对象
    :return:
    """

    # 先获取cookie
    cart_str = request.COOKIES.get('cart')

    # 判断是否有cookie购物车数据
    if cart_str is None:
        # 如果cookie中没有购物车数据,直接返回
        return

    # 把cookie购物车的字符串 转换成字典
    cart_dict = pickle.loads(base64.b64decode(cart_str.encode()))

    # 创建redis连接对象
    redis_conn = get_redis_connection('cart')
    pl = redis_conn.pipeline()

    # 遍历cookie购物车大字典,把sku_id及count向redis的hash中存储
    for sku_id in cart_dict:
        # 把cookie中的sku_id 和count向redis的hash去存储,如果存储的sku_id已存在,就直接覆盖,不存在就是新增
        pl.hset('cart_%d' % user.id, sku_id, cart_dict[sku_id]['count'])
        # 判断当前cookie中的商品是否勾选,如果勾选直接把勾选的商品sku_id 存储到set集合
        if cart_dict[sku_id]['selected']:
            pl.sadd('selected_%d' % user.id, sku_id)

    pl.execute()  # 执行管道

    # 删除cookie购物车数据
    response.delete_cookie('cart')  # 删除cookie




"""
{
    1: {'count': 1, 'selected': True},
    16: {'count': 1, 'selected': True}
}
"""