from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint

from .models import OrderItem,Order
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created
# Create your views here.

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            # 保存优惠信息
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # 清空购物车
            cart.clear()
            # 给顾客发一封邮件
            # 用delay方法声明这是一个异步的操作
            # 会被加入celery的队列
            order_created.delay(order.id)
            # 把订单id放进session
            request.session['order_id'] = order.id
            # 重定向到支付页面
            return redirect(reverse('payment:process'))
            
    else:
        form = OrderCreateForm()
    return render(request,
                  'orders/order/create.html',
                  {'cart':cart,'form':form})


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,
                  'admin/orders/order/detail.html',
                  {'order':order})


@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html',
                            {'order':order})
    response = HttpResponse(content_type = 'application/pdf')
    # 声明首部
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    weasyprint.HTML(string=html).write_pdf(response,
    stylesheets=[weasyprint.CSS(settings.STATIC_ROOT+'\\css\\pdf.css')])
    return response

