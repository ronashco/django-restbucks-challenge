from django.contrib import admin
from nested_inline.admin import NestedTabularInline, NestedModelAdmin

from .models import Option, OptionSet, Product


class OptionTabularInline(NestedTabularInline):
    model = Option
    extra = 1


class OptionSetTabularInline(NestedTabularInline):
    model = OptionSet
    inlines = [OptionTabularInline]
    extra = 1


class ProductAdmin(NestedModelAdmin):
    model = Product
    list_display = ['name']
    inlines = [OptionSetTabularInline]


admin.site.register(Product, ProductAdmin)
