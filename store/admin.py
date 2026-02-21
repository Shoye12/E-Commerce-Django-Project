from django.contrib import admin
from .models import Category, Product, Cart, Order
from .models import Product, Category

class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'price', 'category', 'description']


admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart)
admin.site.register(Order)
