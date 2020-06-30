from django.contrib import admin
from parler.admin import TranslatableAdmin

from .models import Category, Product
# Register your models here.

@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    list_display = ['name','slug']
    # 这表示slug是用name自动生成的
    # prepopulated_fields = {'slug':('name',)}
    # 上面的之所以注释，是因为parler不支持，换成下面的方式了

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug':('name',)}

@admin.register(Product)
class ProductAdmin(TranslatableAdmin):
    list_display = ['name','slug','price',
                    'available','created','updated']
    list_filter = ['available','created','updated']
    # 这里面列出的字段必须也是list_display里面的
    # 它允许我们在展示页直接修改这些字段的值，非常方便
    list_editable = ['price','available']
    # prepopulated_fields = {'slug':('name',)}

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug':('name',)}


