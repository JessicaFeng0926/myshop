# 把celery导进来，这样每次django启动，它也被加载了
from .celery import app as celery_app