from django.urls import path

from . import views

app_name = 'shop'

urlpatterns = [
    # 全部商品列表
    path('',views.product_list,name='product_list'),
    # 指定目录的商品列表
    path('<slug:category_slug>/',
         views.product_list,
         name='product_list_by_category'),
    # 商品详情
    path('<int:id>/<slug:slug>/',
         views.product_detail,
         name='product_detail'),
]