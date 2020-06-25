import csv
import datetime

from django.contrib import admin
from django.http import HttpResponse
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Order, OrderItem
# Register your models here.

def order_detail(obj):
    url = reverse('orders:admin_order_detail',args=[obj.id])
    return mark_safe(f'<a href="{url}">View</a>')

def order_pdf(obj):
    url = reverse('orders:admin_order_pdf',args=[obj.id])
    return mark_safe(f'<a href="{url}">PDF</a>')

# 定义了这个字段的名字
order_pdf.short_description = 'Invoice'

class OrderItemInline(admin.TabularInline):
    '''这个创建成了一个内联类'''
    model = OrderItem
    raw_id_fields = ['product'] 

def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    content_disposition = f'attachment; filename={opts.verbose_name}.csv'
    # 指明了MIME类型
    response = HttpResponse(content_type='text/csv')
    # 在首部添加了信息，指明这个响应包含附件
    response['Content-Disposition'] = content_disposition
    writer = csv.writer(response)

    fields = [field for field in opts.get_fields() \
        if not field.many_to_many and not field.one_to_many]

    # 写csv表头
    writer.writerow([field.verbose_name for field in fields])
    # 把数据写进csv
    for obj  in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')

            data_row.append(value)
        writer.writerow(data_row)
    return response

export_to_csv.short_description = 'Export to CSV'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','first_name','last_name',
                    'email','address','postal_code',
                    # 最后两个字段是上面定义的函数
                    'city','paid','created','updated',
                    order_detail,order_pdf]
    list_filter = ['paid','created','updated']
    # 声明内联类以后，在编辑一个Order对象的时候，
    # 它关联的内联类对象也会出现在编辑页面，
    # 可以同步编辑，非常方便
    inlines = [OrderItemInline]
    # 这允许管理员进行批量导出csv的操作
    actions = [export_to_csv]

