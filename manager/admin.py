from django.contrib import admin
from .models import Product,Order,Order_item,Customer,Varient,Option

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'customer','status','consume_location','datetime']



admin.site.register(Product,ProductAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(Option)
admin.site.register(Varient)
admin.site.register(Customer)
admin.site.register(Order_item)
