from django.urls import path
from master.views import CountryListAV, CategoryListAV

api_url_pattern = [
    path("api/countries", CountryListAV.as_view(), name="api_countries"),
    path("api/categories", CategoryListAV.as_view(), name="api_categories"),
]