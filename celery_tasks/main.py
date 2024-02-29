#celery启动文件
from celery import Celery

#1.创建celery实例对象
celer_app=Celery('my_mall')
#2.加载配置文件
celer_app.config_from_object('celery_tasks.config')
#3.自动注册异步任务
celer_app.autodiscover_tasks(['celery_tasks.sms'])





#启动命令   celery -A celery_tasks.main worker -l info -P eventlet

