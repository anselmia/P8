from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from account.forms import ConnexionForm, RegisterForm
from home.forms import SearchForm
from django.shortcuts import render, redirect
from .models import User
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from substitute.models import Substitute
from django.contrib.auth.decorators import login_required

@login_required
def favorites(request):
    """method to add a product to favorite products"""
    if request.user.is_authenticated:
        current_user = request.user
        favorites = Substitute.objects.filter(user_id=current_user.id).order_by('id')
        
        return render(request, 'favorites.html', locals())
    else:
        messages.error(request, 'Vous devez être connecté pour voir cette page.')
        return render(request, 'home.html', locals())

@login_required
def profile(request):
    """method to show the user's profile"""
    if request.user.is_authenticated:
       return render(request, 'profile.html', locals())
    else:
        messages.error(request, 'Vous devez être connecté pour voir cette page.')
        return render(request, 'login.html', locals())
 
def login(request):    
    if request.method == 'POST':
        form = ConnexionForm(request.POST)
        try:
            if form.is_valid():
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password"]
                user = authenticate(username=username, password=password)  # Nous vérifions si les données sont correctes
                if user:  # Si l'objet renvoyé n'est pas None
                    auth_login(request, user)  # nous connectons l'utilisateur
                    messages.success(request, 'Vous êtes connecté ' + username)
                    request.session.set_expiry(900) 
                    return render(request, 'login.html', locals())
                else:
                    messages.error(request, 'Mauvais login/mot de passe.')  
                    return render(request, 'login.html', locals())
        except Exception as e:
            messages.error(request, 'Mauvais login/mot de passe.')  
            return render(request, 'login.html', locals())
    else:
        form = ConnexionForm(None)

    return render(request, 'login.html', locals())

def register(request):
    error = False
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        try:
            if form.is_valid():
                mail = form.cleaned_data['email']
                username = form.cleaned_data['user_name']
                raw_password = form.cleaned_data['password']              
                try:
                    user = User.objects.create_user(username, mail, raw_password)
                    user.save()
                    
                except Exception as e: 
                    messages.error(request, 'Votre compte n\'a pas été crée.')

                return render(request, 'register.html', locals())

        except Exception as e: 
            print(e)
            messages.error(request, 'Votre compte n\'a pas été crée.')
            return render(request, 'register.html', locals())
    else:
        form = RegisterForm(None)
    
    return render(request,'register.html', locals())

@login_required
def logout(request):
    auth_logout(request)
    return redirect(reverse('home:index'))
    #return render(request, 'home.html', {'form': SearchForm(), 'message': "Vous êtes à présent déconnecté"})