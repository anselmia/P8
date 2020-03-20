from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Product, Favorite
from .api_com import OpenFoodFactsApi
import re

def home(request):
    return render(request, 'home.html')

def search(request):
    if request.method == 'POST':
        if "next" in request.POST:
            value = {}
            value['next'] = request.POST.get('next', None)
            finalvalue = ast.literal_eval(value['next'])
            categorie = OFFA.select_categorie(finalvalue['info'][0])
            context = {'products': OFFA.get_results_from_category(categorie, finalvalue['info'][1]),
                       'firstproduct': value['next']}
            print(context)
            print(context)
            return render(request, 'substitute.html', context, {'title': 'Descriptif'})
    return render(request, 'substitute.html', {'title': 'Résultats'})

def product(request):
    value = {}
    value['info'] = request.POST.get('info', None)
    context = {
        'product': ast.literal_eval(value['info'])}
    return render(request, 'product.html', context, {'title': 'Descriptif'})

def searchnova(request):
    if request.method == 'POST':
        if "next" in request.POST:
            value = {}
            value['next'] = request.POST.get('next', None)
            finalvalue = ast.literal_eval(value['next'])
            categorie = OFFA.select_categorie(finalvalue['info'][0])
            context = {'foods': OFFA.get_results_from_category_nova(categorie, finalvalue['info'][
                1]),
                       'firstfood': value['next']}
            return render(request, 'search.html', context, {'title': 'Descriptif'})
    return render(request, 'search.html', {'title': 'Résultats'})

def substitute(request):
    if request.method == 'GET':
        query = request.GET.get('text')
        if query:
            if re.search('[a-zA-Z]', query):
                results = OFFA.get_results_from_search(query)
                if results:
                    context = {'substitutes': results}
                    return render(request, 'substitute.html', context, {'title': 'Substitute'})
                else:   
                    context = {'message': 'noresults'}
                    return render(request, 'home.html', context)
            else:
                context = {'message': 'noresults'}
                return render(request, 'home.html', context)

OFFA = OpenFoodFactsApi()

def test_granpy():
    """ Module test """
    OFFA = OpenFoodFactsApi()
    grandpy = OFFA.get_results_from_search("Paris")
    bot_response = grandpy.get_response()

if __name__ == "__main__":
    test_granpy()