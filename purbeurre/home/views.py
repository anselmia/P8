from django.shortcuts import render
from django.template import loader
from django.urls import reverse
import re
import logging
from .forms import SearchForm
from . import search as S
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Product
from django.contrib import messages

# Create your views here.

def home(request):    
    context = {'form':SearchForm(None), 'GoToProduct':False}
    return render(request, 'home.html', context)

def search(request):
    context = {}
    form = None
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid(): 
            text = form.cleaned_data['search']
            request.session['text'] = text
    else: 
        form = SearchForm(None) 
        text = request.session['text']
           
    products = S.search_product(text)        

    if products.count() > 0:
        GoToProduct = True
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        products = paginator.get_page(page)
        context['products'] = products
    else:
        messages.warning(request, "Il n'y a aucun résultat avec ces termes. Essayez encore !")
        GoToProduct = False

    context['GoToProduct'] = GoToProduct
    context['form'] = form
    
    return render(request, 'home.html', context)
    
l = logging.getLogger('django.db.backends')
l.setLevel(logging.DEBUG)
l.addHandler(logging.StreamHandler())