#celery启动文件
from celery import Celery

#1.创建celery实例对象
celery_app=Celery('my_mall')
#2.加载配置文件
celery_app.config_from_object('celery_tasks.config')
#3.自动注册异步任务
celery_app.autodiscover_tasks(['celery_tasks.sms'])
# ,'celery_tasks.html','celery_tasks.index'




#启动命令   celery -A celery_tasks.main worker -l info -P eventlet

