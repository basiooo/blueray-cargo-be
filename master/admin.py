from django.contrib import admin
from master.models import Country, Category


class CountryAdmin(admin.ModelAdmin):
    list_display = ("name", "flag", "currency")


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("country", "title", "price_per_kilo")


admin.site.register(Country, CountryAdmin)
admin.site.register(Category, CategoryAdmin)
