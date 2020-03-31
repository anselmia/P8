from django import forms
from account.models import User
from django.contrib.auth.forms import UserChangeForm, UserCreationForm


class ConnexionForm(forms.Form):
    username = forms.CharField(
        label="Nom d'utilisateur",
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "username",
                "class": "form-control",
                "name": "username",
                "id": "inputUsername",
            }
        ),
    )
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(
            attrs={
                "type": "password",
                "id": "inputPassword",
                "name": "password",
                "class": "form-control",
            }
        ),
    )


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254, help_text="Rentrer une adresse email valide"
    )
    robot = forms.BooleanField(required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("username", "email")
