from django.contrib import admin

# Register your models here.
from coffeeshop.models import Product, CustomizableAttribute, CustomizableAttributeOption, Order, OrderItem
from coffeeshop.utils.admin_panel import admin_changelist_link, admin_link
from django_fsm import can_proceed


class CustomizableAttributeInline(admin.StackedInline):
    model = CustomizableAttribute
    extra = 1
    fields = ('name',)


class CustomizableAttributeOptionInline(admin.StackedInline):
    model = CustomizableAttributeOption
    extra = 1
    fields = ('name',)


class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 1
    fields = ('product', 'count', 'selected_options')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'unit_price']
    list_display_links = ['product_name']
    search_fields = ['product_name']
    list_per_page = 250
    list_max_show_all = 1000
    prepopulated_fields = {'slug': ['product_name']}

    # @admin_changelist_link(
    #     'customizable_attributes',
    #     'customizable attributes',
    #     query_string=lambda c: 'product_set__id={}'.format(c.pk)
    # )
    # def get_attributes(self, section):
    #     return 'customizable attributes'


@admin.register(CustomizableAttribute)
class CustomizableAttributeAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_options']
    list_display_links = ['name']
    search_fields = ['name']
    inlines = [CustomizableAttributeOptionInline]

    @admin_changelist_link(
        'options',
        'options',
        query_string=lambda c: 'attribute_id={}'.format(c.pk)
    )
    def get_options(self, section):
        return 'options'


@admin.register(CustomizableAttributeOption)
class CustomizableAttributeOptionAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_attribute']
    list_display_links = ['name']
    search_fields = ['name']

    @admin_link('attribute', 'CustomizableAttribute')
    def get_attribute(self, attribute):
        return attribute.name


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'state']
    list_display_links = ['id']
    inlines = [OrderItemInline]
    actions = ['make_prepare', 'make_ready', 'make_delivered', 'make_canceled']
    readonly_fields = ('state',)

    def make_prepare(self, request, queryset):
        for order in queryset.all():
            if can_proceed(order.prepare):
                order.prepare()
                order.save()

    def make_ready(self, request, queryset):
        for order in queryset.all():
            if can_proceed(order.ready):
                order.ready()
                order.save()

    def make_delivered(self, request, queryset):
        for order in queryset.all():
            if can_proceed(order.deliver):
                order.deliver()
                order.save()

    def make_canceled(self, request, queryset):
        for order in queryset.all():
            if can_proceed(order.cancel):
                order.cancel()
                order.save()

    # def get_actions(self, request):
    #     actions = super().get_actions(request)
    #     queryset = super().get_queryset(request)
    #     for order in queryset.all():
    #         if not can_proceed(order.prepare):
    #             actions.pop('make_prepare', None)
    #         if not can_proceed(order.ready):
    #             actions.pop('make_ready', None)
    #         if not can_proceed(order.deliver):
    #             actions.pop('make_delivered', None)
    #         if not can_proceed(order.cancel):
    #             actions.pop('make_canceled', None)
    #     return actions
