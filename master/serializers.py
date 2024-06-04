from rest_framework import serializers
from master.models import Country, Category


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"
