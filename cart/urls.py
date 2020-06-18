from django.urls import path

from . import views

app_name = 'cart'

urlpatterns = [
    # 展示购物车详情
    path('',views.cart_detail,name='cart_detail'),
    # 添加商品
    path('add/<int:product_id>',views.cart_add,name='cart_add'),
    # 移除商品
    path('remove/<int:product_id>',views.cart_remove,
         name='cart_remove'),
]