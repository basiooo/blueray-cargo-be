from rest_framework import generics, response, status, exceptions
from master.serializers import (
    CountrySerializer,
    CategorySerializer,
    CalculationSerializer,
)
from master.models import Country, Category
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import (
    permission_classes,
    authentication_classes,
    api_view,
)
from master.external_call import get_cities, get_cost
from master.utils import search_city_by_name
from django.core.cache import cache
import json


@permission_classes([IsAuthenticated])
class CountryListAV(generics.ListAPIView):
    serializer_class = CountrySerializer
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        search = self.request.query_params.get("search")
        country = Country.objects
        if search:
            country = country.filter(name__contains=search)
        return country.all()


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def destination(request):
    cities = cache.get("rajaongkir_cities")
    if not cities:
        cities = get_cities()
        if len(cities) > 0:
            cache.set("rajaongkir_cities", cities)
    search = request.query_params.get("search")
    if search:
        cities = search_city_by_name(search, cities)
    return response.Response({"city": cities})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def calculation(request):
    body = json.loads(request.body)

    serialize = CalculationSerializer(data=body)
    if not serialize.is_valid():
        return response.Response(serialize.errors, status=status.HTTP_400_BAD_REQUEST)
    data = serialize.data

    # set local origin 444 code for surabaya
    local_origin_id = 444
    req_body = {
        "origin": local_origin_id,
        "destination": data.get("destination_id"),
        "weight": data.get("weight", 0),
        "courier": "jne",
    }
    api_result = get_cost(req_body)
    if api_result is None:
        return response.Response(
            {"error": "error get info from raja ongkir api"},
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )
    country = Country.objects.get(pk=data.get("country_id"))
    category = Category.objects.get(pk=data.get("category_id"))
    international_price = data.get("weight", 0) * category.price_per_kilo
    result = api_result.get("results")[0]  # get first result
    domestic_price = result.get("costs")[0].get("cost")[0].get("value")
    res = {
        "origin": {
            "name": country.name,
            "flag": country.flag,
        },
        "destination": api_result.get("destination_details"),
        "category_name": category.title,
        "international_price": international_price,
        "domestic_price": domestic_price,
        "total_price": domestic_price + international_price,
    }
    return response.Response(res, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
class CategoryListAV(generics.ListAPIView):
    serializer_class = CategorySerializer
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        category = Category.objects
        search = self.request.query_params.get("search")
        country_id = self.request.query_params.get("country_id")
        if country_id:
            try:
                int(country_id)
            except Exception:
                return category.none()
            category = category.filter(country_id=country_id)
        if search:
            category = category.filter(title__contains=search)
        return category.all()
