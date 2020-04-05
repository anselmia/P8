from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .forms import ConnexionForm, UserUpdateForm, SignUpForm
from home.forms import SearchForm
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from substitute.models import Substitute
from django.contrib.auth.decorators import login_required


@login_required
def favorites(request):
    """method to add a product to favorite products"""
    favoris = Substitute.objects.filter(user_id=request.user)
    return render(
        request,
        "favorites.html",
        {"favoris": favoris,
        "form_search": SearchForm(None)}
    )


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
        except:  # pragma: no cover
            messages.error(
                request,
                "Erreurs durant l'enregistrement des informations de votre profil",
            )
    else:
        form = UserUpdateForm(instance=request.user)

    return render(
        request,
        "profile.html",
        {"form": form, "form_search": SearchForm(None)}
    )


def login(request):
    if request.user.is_authenticated:
        return redirect(reverse("home:index"))
    else:
        if request.method == "POST":
            form = ConnexionForm(request.POST)
            try:
                if form.is_valid():
                    user = authenticate(
                        username=form.cleaned_data["username"], password=form.cleaned_data["password"]
                    )
                    try:
                        if user:
                            auth_login(request, user)
                            request.session.set_expiry(900)
                            return HttpResponseRedirect(request.session["previous"])
                        else:
                            messages.error(request, "Mauvais login/mot de passe.")
                            return render(request, "login.html", {"form": form})
                    except:  # pragma: no cover
                        redirect(reverse('home:index'))
            except Exception as e:  # pragma: no cover
                messages.error(request, "Erreur de login.")
                return render(request, "login.html", {"form": form})
        else:
            form = ConnexionForm(None)
            request.session["previous"] = request.META.get("HTTP_REFERER")

        return render(
            request,
            "login.html",
            {"form": form, "form_search": SearchForm(None)}
        )


def register(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        try:
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get("username")
                raw_password = form.cleaned_data.get("password1")
                user = authenticate(username=username, password=raw_password)
                auth_login(request, user)
                return redirect(reverse("home:index"))

        except Exception as e:
            messages.error(request, "Votre compte n'a pas été crée.")
    else:
        form = SignUpForm(None)

    return render(
        request,
        "register.html",
        {"form": form, "form_search": SearchForm(None)}
    )


@login_required
def logout(request):
    auth_logout(request)
    return redirect(reverse("home:index"))
