import os

from celery import Celery

# 设置默认的django settings,这是给Celery的命令行用的
os.environ.setdefault('DJANGO_SETTINGS_MODULE','myshop.settings')

app = Celery('myshop')

# 第二个参数指明了在settings里所有跟Celery相关的配置
# 都有一个CELERY_前缀
app.config_from_object('django.conf:settings',namespace='CELERY')
# Celery会自动寻找异步任务
# 它会查看每个app里的tasks.py文件
app.autodiscover_tasks()