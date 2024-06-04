from django.urls import path

from authentication.views import registration, ApiRegistration

urlpatterns = [
    path("register/", registration, name="register"),
]
