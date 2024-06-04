from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    flag = models.CharField(max_length=255, null=False, blank=False)
    currency = models.CharField(max_length=255, null=False, blank=False)

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Country"


class Category(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=False, blank=False)
    price_per_kilo = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Category"
