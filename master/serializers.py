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


class CalculationSerializer(serializers.Serializer):
    weight = serializers.IntegerField()
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    country_id = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all())
    destination_id = serializers.IntegerField()
