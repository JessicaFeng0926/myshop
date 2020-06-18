from django.contrib import admin

from .models import Category, Product
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','slug']
    # 这表示slug是用name自动生成的
    prepopulated_fields = {'slug':('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','slug','price',
                    'available','created','updated']
    list_filter = ['available','created','updated']
    # 这里面列出的字段必须也是list_display里面的
    # 它允许我们在展示页直接修改这些字段的值，非常方便
    list_editable = ['price','available']
    prepopulated_fields = {'slug':('name',)}


