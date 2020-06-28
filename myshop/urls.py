"""myshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _

# 这些路由都加上了语言前缀
urlpatterns = i18n_patterns(
    path(_('admin/'), admin.site.urls),
    # 购物车的路由一定要放到主页路由的前面，因为它的限制更多
    # 如果主页放到前面，就无法找到购物车的路由了
    path(_('cart/'),include('cart.urls',namespace='cart')),
    # 订单路由
    path(_('orders/'),include('orders.urls',namespace='orders')),
    # 支付路由
    path(_('payment/'),include('payment.urls',namespace='payment')),
    # 优惠券
    path(_('coupons/'),include('coupons.urls',namespace='coupons')),
    # 翻译接口路由
    path('rosetta/',include('rosetta.urls')),
    path('',include('shop.urls',namespace='shop')),
)

# 只有在开发环境才使用这个媒体文件路径，不适合在生产环境使用
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
