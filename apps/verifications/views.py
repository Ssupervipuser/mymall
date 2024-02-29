from random import randint

from django.shortcuts import render
from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
# Create your views here.
from libs.yuntongxun.sms import CCP
from utils.exceptions import logger
from .constaints import *
from celery_tasks.sms.tasks import send_sms_code
class SMSCodeView(APIView):
    """发送短信验证码"""

    def get(self, request, mobile):
        # 1创建连接到redis的对象
        redis_conn = get_redis_connection('verify_codes')
        #2先从redis获取发送标记
        send_flag=redis_conn.get('send_flag_%s' % mobile)
        if send_flag:
            return Response({"message": "发送短信过于频繁"}, status=status.HTTP_400_BAD_REQUEST)
        # 3生成和发送短信验证码
        sms_code = '%06d' % randint(0,999999)
        logger.info(sms_code)

        # 2以下代码演示redis管道pipeline的使用
        pl = redis_conn.pipeline()


        # 4将验证码保存到redis中
        pl.setex('sms_%s' % mobile, SMS_CODE_REDIS_EXPIRES, sms_code)
        # 5存储标记
        pl.setex('send_flag_%s' % mobile, SEND_SMS_CODE_INTERVAL, 1)
        #执行管道
        pl.execute()
        # 6CCP(),send_template_sms(self,手机号，[验证码，5],1)：
        # CCP().send_template_sms(mobile, [sms_code, SMS_CODE_REDIS_EXPIRES//60], 1)
        #触发异步任务，将异步任务添加到celery任务队列
        send_sms_code.delay(mobile,sms_code)

        # 响应发送短信验证码结果
        return Response({"message": "OK"})

