from django.contrib import admin
from .models import Customer


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password', 'email',)}),)


admin.site.register(Customer, CustomerAdmin)
