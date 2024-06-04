from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, unique=True)
    flag = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        unique=True,
        help_text="static url for this flag",
    )
    currency = models.CharField(max_length=255, null=False, blank=False, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Country"


class Category(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=False, blank=False)
    price_per_kilo = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Category"
