from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .forms import ConnexionForm, UserUpdateForm, SignUpForm
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from substitute.models import Substitute
from django.contrib.auth.decorators import login_required


@login_required
def favorites(request):
    """method to add a product to favorite products"""
    favoris = Substitute.objects.filter(user_id=request.user)
    return render(request, "favorites.html", {"favoris": favoris})


@login_required
def profile(request):
    """Allow the user to view their account information."""

    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=request.user)
        try:
            if form.is_valid():
                form.save()
                messages.success(
                    request,
                    "Les modifications de votre profil ont bien été enregistrées",
                )
        except:
            messages.error(
                request,
                "Erreurs durant l'enregistrement des informations de votre profil",
            )
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, "profile.html", {"form": form})


def login(request):
    if request.user.is_authenticated:
        return redirect(reverse("home:index"))
    else:
        if request.method == "POST":
            form = ConnexionForm(request.POST)
            try:
                if form.is_valid():
                    username = form.cleaned_data["username"]
                    password = form.cleaned_data["password"]
                    user = authenticate(
                        username=username, password=password
                    )  # Nous vérifions si les données sont correctes
                    if user:  # Si l'objet renvoyé n'est pas None
                        auth_login(request, user)  # nous connectons l'utilisateur
                        request.session.set_expiry(900)
                        return HttpResponseRedirect(request.session["previous"])
                    else:
                        messages.error(request, "Mauvais login/mot de passe.")
                        return render(request, "login.html", {"form": form})
            except Exception as e:
                messages.error(request, "Erreur de login.")
                return render(request, "login.html", {"form": form})
        else:
            form = ConnexionForm(None)
            request.session["previous"] = request.META.get("HTTP_REFERER")

        return render(request, "login.html", {"form": form})


def register(request):
    error = False
    if request.method == "POST":
        form = SignUpForm(request.POST)
        try:
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get("username")
                raw_password = form.cleaned_data.get("password1")
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return redirect(reverse("home:index"))

        except Exception as e:
            messages.error(request, "Votre compte n'a pas été crée.")
    else:
        form = SignUpForm(None)

    return render(request, "register.html", locals())


@login_required
def logout(request):
    auth_logout(request)
    return redirect(reverse("home:index"))
