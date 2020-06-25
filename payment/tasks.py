from io import BytesIO

from celery import task
import weasyprint
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

from orders.models import Order


@task
def payment_completed(order_id):
    '''这个任务是在用户成功付款之后
    把电子发票用邮件发给用户'''
    order = Order.objects.get(id=order_id)

    # 创建发票邮件
    subject = f'My Shop - EE Invoice no. {order.id}'
    message = 'Please, find attached the invoice for your recent purchase.'
    email = EmailMessage(subject,
                         message,
                         'admin@myshop.com',
                         [order.email])
    
    # 生成PDF并添加为邮件的附件
    html = render_to_string('orders/order/pdf.html',
                            {'order':order})
    out = BytesIO()
    stylesheets = [weasyprint.CSS(settings.STATIC_ROOT+'\\css\\pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out,
                                           stylesheets=stylesheets)
    email.attach(f'order_{order.id}.pdf',
                 out.getvalue(),
                 'application/pdf')
    
    # 发邮件
    email.send()