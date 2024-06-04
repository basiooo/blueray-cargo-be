from rest_framework import generics
from master.serializers import CountrySerializer, CategorySerializer
from master.models import Country, Category
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes


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
