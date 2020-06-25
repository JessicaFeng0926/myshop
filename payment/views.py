import braintree
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings

from orders.models import Order
from .tasks import payment_completed

# Create your views here.

# 实例化braintree支付网关
gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)

def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order,id=order_id)
    total_cost = order.get_total_cost()

    if request.method == 'POST':
        # 取出随机数，这是在client_token已经被提交之后
        # 这个随机数是Braintree Javascript SDK生成的
        nonce = request.POST.get('payment_method_nonce',None)
        # 创建并且提交事务
        result = gateway.transaction.sale({
            'amount':f'{total_cost:.2f}',
            'payment_method_nonce':nonce,
            'options':{
                # 把这个选项设为True，这个事务就会自动提交结算
                'submit_for_settlement':True
            }
        })
        if result.is_success:
            # 把订单标记为已支付
            order.paid = True
            # 保存事务id
            order.braintree_id = result.transaction.id
            order.save()
            # 异步发送一封附有发票的邮件
            payment_completed.delay(order.id)
            return redirect('payment:done')
        else:
            return redirect('payment:canceled')
    else:
        # 生成口令,这才是支付的第一步
        client_token = gateway.client_token.generate()
        return render(request,
                      'payment/process.html',
                      {'order':order,
                      'client_token':client_token})

def payment_done(request):
    '''支付成功后显示的页面'''
    return render(request,
                  'payment/done.html')

def payment_canceled(request):
    '''支付取消后显示的页面'''
    return render(request,
                  'payment/canceled.html')