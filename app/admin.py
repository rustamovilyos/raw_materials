from django.contrib import admin
from .models import Product, Order, OrderProduct


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'product_image')
    list_filter = ('price', 'quantity')
    search_fields = ('name', 'price')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('date_ordered', 'name', 'email', 'phone', 'address')
    list_filter = ('date_ordered', 'products', 'name')
    search_fields = ('name', 'email', 'phone', 'address', 'products')


class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity')
    list_filter = ('order', 'product')
    search_fields = ('order', 'product')


admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)

