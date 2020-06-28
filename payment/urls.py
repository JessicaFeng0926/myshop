from django.urls import path
from django.utils.translation import gettext_lazy as _

from . import views

app_name = 'payment'

urlpatterns = [
    # 处理支付
    path(_('process/'),views.payment_process,name='process'),
    # 支付完成
    path(_('done/'),views.payment_done,name='done'),
    # 支付取消
    path(_('canceled/'),views.payment_canceled,name='canceled'),
]