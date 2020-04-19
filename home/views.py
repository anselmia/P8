""" Home Views """

from django.shortcuts import render
from .forms import SearchForm
from . import search as S
from django.core.paginator import Paginator
from django.contrib import messages
from home.management.update_db import update_product

# Create your views here.


def home(request):
    """
    Views for home
    :param request:
    :return render home.html:
    """
    update_product()
    return render(
        request, "home.html", {"form_search": SearchForm(None), "GoToProduct": False}
    )


def mentions(request):
    """
    Views for mentions
    :param request:
    :return render mentions.html:
    """
    return render(request, "mentions.html", {"form_search": SearchForm(None)})


def search(request):
    """
    Views for search
    :param request:
    Search product form user input text
    :return render home.html:
    """
    context = {}
    form = None
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data["search"]
            request.session["text"] = text
    else:
        form = SearchForm(None)
        text = request.session["text"]

    products = S.search_product(text)

    if products.count() > 0:
        GoToProduct = True
        paginator = Paginator(products, 6)
        page = request.GET.get("page")
        products = paginator.get_page(page)
        context["products"] = products
    else:
        messages.warning(
            request, "Il n'y a aucun résultat avec ces termes. Essayez encore !"
        )
        GoToProduct = False

    context["GoToProduct"] = GoToProduct
    context["form_search"] = form

    return render(request, "home.html", context)
