from django.contrib.auth import get_user_model
from django.contrib.auth.forms import BaseUserCreationForm
from django.contrib.auth.models import User
from django.forms.fields import EmailField


class RegisterForm(BaseUserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("email",)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        if commit:
            user.save()
            if hasattr(self, "save_m2m"):
                self.save_m2m()
        return user
