from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=UserModel.objects.all())]
    )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )

    class Meta:
        model = UserModel
        fields = ("password", "email", "first_name", "last_name")

    def create(self, validated_data):
        user = UserModel.objects.create(
            email=validated_data["email"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user
