from django.shortcuts import render
import logging
from .forms import SearchForm
from . import search as S
from django.core.paginator import Paginator
from django.contrib import messages

# Create your views here.


def home(request):
    return render(
        request, "home.html", {"form": SearchForm(None), "GoToProduct": False}
    )


def search(request):
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
    context["form"] = form

    return render(request, "home.html", context)


# l = logging.getLogger('django.db.backends')
# l.setLevel(logging.DEBUG)
# l.addHandler(logging.StreamHandler())
