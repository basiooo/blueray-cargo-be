"""
URL configuration for blueray project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from authentication.views import ApiRegistration
from master.urls import api_url_pattern as master_api_url
from django.views.generic import RedirectView
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path("",RedirectView.as_view(url="/admin")),
    path("admin/", admin.site.urls),
    path("auth/", include("authentication.urls")),
    path("api/token/", TokenObtainPairView.as_view(), name="api_token_obtain_pair"),
    path("api/register/", ApiRegistration.as_view(), name="api_register"),
    path("api/token/refresh", TokenRefreshView.as_view(), name="api_token_refresh"),
] + master_api_url + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

