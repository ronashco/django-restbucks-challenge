from django.contrib import admin
from .models import Customer
from OrderManagement.models import Product, CustomizedProduct, OrderLine, Order


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password', 'email',)}),)


class CustomizedProductAdmin(admin.TabularInline):
    model = CustomizedProduct


class ProductAdmin(admin.ModelAdmin):
    inlines = [
        CustomizedProductAdmin,
    ]


class OrderLineAdmin(admin.TabularInline):
    model = OrderLine


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_time', 'status')
    inlines = [
        OrderLineAdmin,
    ]


admin.site.register(Product, ProductAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Order, OrderAdmin)
