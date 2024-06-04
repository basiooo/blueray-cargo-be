from django.http import HttpResponseNotAllowed
from django.shortcuts import redirect, render

# Create your views here.
from django.urls import reverse
from rest_framework import generics

from authentication.forms import RegisterForm
from authentication.serializers import RegisterSerializer
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class ApiRegistration(generics.CreateAPIView):
    serializer_class = RegisterSerializer


def registration(request):
    context = {"title": "Register"}
    if request.user.is_authenticated:
        return redirect(reverse("admin:index"))
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("admin:login"))
    elif request.method == "GET":
        form = RegisterForm()
    else:
        return HttpResponseNotAllowed()
    context.update({"form": form})
    return render(request, "register.html", context)
