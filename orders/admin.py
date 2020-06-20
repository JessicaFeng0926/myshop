from django.contrib import admin

from .models import Order, OrderItem
# Register your models here.

class OrderItemInline(admin.TabularInline):
    '''这个创建成了一个内联类'''
    model = OrderItem
    raw_id_fields = ['product'] 


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','first_name','last_name',
                    'email','address','postal_code',
                    'city','paid','created','updated']
    list_filter = ['paid','created','updated']
    # 声明内联类以后，在编辑一个Order对象的时候，
    # 它关联的内联类对象也会出现在编辑页面，
    # 可以同步编辑，非常方便
    inlines = [OrderItemInline]
