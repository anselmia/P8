from django.test import TestCase
from django.urls import reverse
from .forms import SearchForm
from .models import Product, Category
from django.contrib.messages import get_messages


# Create your tests here.
class HomeTests(TestCase):
    def test_login_page(self):  # pragma: no cover
        response = self.client.get("/")
        self.assertEquals(response.status_code, 200)

    def test_view(self):  # pragma: no cover
        response = self.client.get(reverse("home:index"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")


class SearchTests(TestCase):
    def setUp(self):  # pragma: no cover
        Category.objects.create(name="test")
        category = Category.objects.get(name="test")
        for index in range(0, 9):
            Product.objects.create(
                name=f"My product {index}",
                category_id=category,
                nutriscore=index,
                url=f"www.test.fr {index}",
                ingredients="www.test.fr",
                photo="www.test.fr",
                fat_100g=0,
                saturate_fat_100g=0,
                salt_100g=0,
                sugars_100g=0,
            )

    def test_search_page(self):  # pragma: no cover
        response = self.client.post("/product/", {"search": "product"}, follow=True)
        self.assertEquals(response.status_code, 200)

    def test_view(self):  # pragma: no cover
        response = self.client.post(
            reverse("home:search"), {"search": "product"}, follow=True
        )
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")

    def test_SearchForm_valid(self):  # pragma: no cover
        form = SearchForm(data={"search": "product"})
        self.assertTrue(form.is_valid())

    def test_SearchForm_invalid(self):  # pragma: no cover
        form = SearchForm(data={"search": ""})
        self.assertFalse(form.is_valid())

    def test_search_noresult(self):  # pragma: no cover
        response = self.client.post(
            reverse("home:search"), {"search": "dfsdfcds"}, follow=True
        )
        # should be logged in now
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            "Il n'y a aucun résultat avec ces termes. Essayez encore !",
        )
        self.assertFalse(response.context["GoToProduct"])
        self.assertFalse(response.context["GoToProduct"] == True)

    def test_search_result(self):  # pragma: no cover
        response = self.client.post(
            reverse("home:search"), {"search": "product"}, follow=True
        )
        # should be logged in now
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 0)
        self.assertTrue(response.context["products"])
        products = response.context["products"]
        self.assertTrue(len(products) > 0)
        self.assertTrue(response.context["GoToProduct"] == True)

    def test_search_pagination(self):  # pragma: no cover
        response = self.client.post("/product/", {"search": "product"}, follow=True)
        response = self.client.get("/product/?page=2", {"page": "2"}, follow=True)
        # should be logged in now
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 0)
        self.assertTrue(response.context["products"])
        products = response.context["products"]
        self.assertTrue(len(products) > 0)
        self.assertTrue(response.context["GoToProduct"] == True)
