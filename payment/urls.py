from django.urls import path

from . import views

app_name = 'payment'

urlpatterns = [
    # 处理支付
    path('process/',views.payment_process,name='process'),
    # 支付完成
    path('done/',views.payment_done,name='done'),
    # 支付取消
    path('canceled/',views.payment_canceled,name='canceled'),
]