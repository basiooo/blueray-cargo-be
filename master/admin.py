from django.contrib import admin
from master.models import Country, Category
from django.utils.html import mark_safe


class CountryAdmin(admin.ModelAdmin):
    list_display = ("name", "get_flag", "currency")

    def get_flag(self, obj):
        return mark_safe(f"<img src='{obj.flag}' alt='{obj.flag}'>")

    get_flag.short_description = "flag"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("country", "title", "price_per_kilo")


admin.site.register(Country, CountryAdmin)
admin.site.register(Category, CategoryAdmin)
