from django.contrib import admin

from .models import Order


class OrderModelAdmin(admin.ModelAdmin):
    list_display = ["id", "status", "location"]
    list_display_links = ["id"]

    class Meta:
        module = Order


admin.site.register(Order, OrderModelAdmin)

