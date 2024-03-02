#编写异步任务代码
from celery_tasks.sms.constaints import SMS_CODE_REDIS_EXPIRES
from celery_tasks.sms.yuntongxun.sms import CCP
from celery_tasks.main import celery_app

#使用装饰器注册任务
@celery_app.task(name='send_sms_code')
def send_sms_code(mobile,sms_code):
    """
    发送短信异步任务
    :param mobile:
    :param sms_code:
    :return:
    """
    CCP().send_template_sms(mobile, [sms_code, SMS_CODE_REDIS_EXPIRES//60], 1)