from django.contrib import admin

from .models import ProductOption, DetailOption, Menu


class MenuModelAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    list_display_links = ["name"]

    class Meta:
        model = Menu


admin.site.register(Menu, MenuModelAdmin)


class ProductionOptionModelAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_display_links = ["name"]

    class Meta:
        model = ProductOption


admin.site.register(ProductOption, ProductionOptionModelAdmin)


class DetailOptionModelAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_display_links = ["name"]

    class Meta:
        model = DetailOption


admin.site.register(DetailOption, DetailOptionModelAdmin)
