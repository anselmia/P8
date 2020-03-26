from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from home import search
from .models import Substitute
from home.models import Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def substitute(request, **kwarg):
    if request.method == 'GET':
        id_product = kwarg['product_id']
        substitutes = search.search_substitute(id_product)
        if substitutes.count() > 0:
            paginator = Paginator(substitutes, 6)
            page = request.GET.get('page')
            substitutes = paginator.get_page(page)
            context = {}
            context['substitutes'] = substitutes
            context['title'] = 'Substitute'
            context['product'] = Product.objects.get(pk=id_product)
            
            return render(request, 'substitute.html', context)
        else:   
            context = {'message': 'noresults'}
            return render(request, 'home.html', context)

def detail(request, **kwarg):
    if request.method == 'GET':
        id_product = kwarg['product_id']
        product = Product.objects.get(pk=id_product)
        if product is not None:
            context = {}
            context['product'] = product
            context['title'] = 'Détails du produit ' + product.name 
            
            return render(request, 'detail.html', context)
        else:   
            context = {'message': 'noresults'}
            return render(request, 'home.html', context)

def save(request, **kwarg):
    pass