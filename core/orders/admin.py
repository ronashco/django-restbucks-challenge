from django.contrib import admin
from .models import Order, OrderProduct


class OrderProductInline(admin.TabularInline):

    model = OrderProduct
    extra = 1

    fields = ('product', 'customization', 'price',)

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(set(
            [field.name for field in self.opts.local_fields] +
            [field.name for field in self.opts.local_many_to_many]
        ))
        if 'is_submitted' in readonly_fields:
            readonly_fields.remove('is_submitted')
        return readonly_fields


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    fields = ('status', 'total_price', 'user', 'date', 'modified', 'location')
    inlines = (OrderProductInline,)
    list_filter = ('status', 'date')

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(set(
            [field.name for field in self.opts.local_fields] +
            [field.name for field in self.opts.local_many_to_many]
        ))
        if 'is_submitted' in readonly_fields:
            readonly_fields.remove('is_submitted')
        readonly_fields.remove('status')
        return readonly_fields
