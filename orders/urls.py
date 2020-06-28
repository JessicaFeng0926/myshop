from django.urls import path
from django.utils.translation import gettext_lazy as _

from . import views

app_name = 'orders'

urlpatterns = [
    path(_('create/'),views.order_create,name='order_create'),
    # 这是只有工作人员可以看的订单详情
    path('admin/order/<int:order_id>/',
         views.admin_order_detail,
         name='admin_order_detail'),
    # 这是开pdf发票的路由
    path('admin/order/<int:order_id>/pdf/',
         views.admin_order_pdf,
         name='admin_order_pdf'),
]