from django.test import TestCase
from unittest.mock import patch
from django.urls import reverse
from account.models import User
from home.models import Product, Category
from .models import Substitute
from django.contrib.messages import get_messages

# Create your tests here.
class SubstituteTests(TestCase):
    def setUp(self):  # pragma: no cover
        Category.objects.create(name="test")
        Category.objects.create(name="test_test")
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
        category_2 = Category.objects.get(name="test_test")
        Product.objects.create(
            name=f"test",
            category_id=category_2,
            nutriscore="a",
            url=f"www.test.fra",
            ingredients="www.test.fra",
            photo="www.test.fra",
            fat_100g=0,
            saturate_fat_100g=0,
            salt_100g=0,
            sugars_100g=0,
        )

    def test_substitute_page(self):  # pragma: no cover
        product = Product.objects.get(name="My product 1")
        response = self.client.get(
            "/substitute/" + str(product.id), args=(product.id,), follow=True
        )
        self.assertEquals(response.status_code, 200)

    def test_view(self):  # pragma: no cover
        product = Product.objects.get(name="My product 1")
        response = self.client.get(
            reverse("substitute:search-a-substitute", args=(product.id,)), follow=True
        )
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "substitute.html")

    def test_search_noresult(self):  # pragma: no cover
        product = Product.objects.get(name="test")
        response = self.client.get(
            reverse("substitute:search-a-substitute", args=(product.id,)), follow=True
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Il n'y a pas de substitut pour ce produit")

    def test_search_result(self):  # pragma: no cover
        product = Product.objects.get(name="My product 1")
        response = self.client.get(
            reverse("substitute:search-a-substitute", args=(product.id,)), follow=True
        )
        product = response.context["product"]
        self.assertEqual(product.name, "My product 1")
        self.assertTrue(response.context["substitutes"])
        substitutes = response.context["substitutes"]
        self.assertTrue(len(substitutes) > 0)

    def test_search_pagination(self):  # pragma: no cover
        product = Product.objects.get(name="My product 1")
        response = self.client.get(
            reverse("substitute:search-a-substitute", args=(product.id,)), follow=True
        )
        response = self.client.get(
            reverse("substitute:search-a-substitute", args=(product.id,)),
            {"page": "2"},
            follow=True,
        )
        self.assertTrue(response.context["product"])
        self.assertTrue(response.context["substitutes"])
        substitutes = response.context["substitutes"]
        self.assertTrue(len(substitutes) > 0 and len(substitutes) < 6)


class DetailTests(TestCase):
    def setUp(self):  # pragma: no cover
        Category.objects.create(name="test")
        Category.objects.create(name="test_test")
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
        self.credentials = {"username": "testuser", "password": "!!!!!!!!"}
        User.objects.create_user(**self.credentials)
        self.client.login(
            username=self.credentials["username"], password=self.credentials["password"]
        )

    def test_detail_page(self):  # pragma: no cover
        product = Product.objects.get(name="My product 1")
        substitute = Product.objects.get(name="My product 2")
        response = self.client.get(
            "/detail/" + str(product.id) + "/" + str(substitute.id),
            args=(product.id, substitute.id,),
            follow=True,
        )
        self.assertEquals(response.status_code, 200)

    def test_view(self):  # pragma: no cover
        product = Product.objects.get(name="My product 1")
        substitute = Product.objects.get(name="My product 2")
        response = self.client.get(
            reverse("substitute:detail", args=(product.id, substitute.id,)), follow=True
        )
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "detail.html")

    def test_detail_no_result(self):  # pragma: no cover
        product = Product.objects.get(name="My product 1")
        response = self.client.get(
            reverse("substitute:detail", args=(product.id, 13,)), follow=True
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            "Il y a eu une lors de la récupération des information du substitut",
        )
        self.assertTemplateUsed(response, "home.html")

    def test_detail_result(self):  # pragma: no cover
        product = Product.objects.get(name="My product 1")
        substitute = Product.objects.get(name="My product 2")
        response = self.client.get(
            reverse("substitute:detail", args=(product.id, substitute.id,)), follow=True
        )
        product = response.context["product"]
        self.assertEqual(product.name, "My product 1")
        product = response.context["substitute"]
        self.assertEqual(product.name, "My product 2")
        self.assertTemplateUsed(response, "detail.html")
        self.assertFalse(response.context["exist"])

    def test_search_favoris_exist(self):  # pragma: no cover
        product = Product.objects.get(name="My product 1")
        substitute = Product.objects.get(name="My product 2")
        user = User.objects.get(username="testuser")
        Substitute.objects.create(
            product_id=product, substitute_id=substitute, user_id=user
        )
        response = self.client.get(
            reverse("substitute:detail", args=(product.id, substitute.id,)), follow=True
        )
        product = response.context["product"]
        self.assertEqual(product.name, "My product 1")
        product = response.context["substitute"]
        self.assertEqual(product.name, "My product 2")
        self.assertTemplateUsed(response, "detail.html")
        self.assertTrue(response.context["exist"])


class SaveTests(TestCase):
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
        self.credentials = {"username": "testuser", "password": "!!!!!!!!"}
        User.objects.create_user(**self.credentials)
        self.client.login(
            username=self.credentials["username"], password=self.credentials["password"]
        )

    def test_save_page(self):  # pragma: no cover
        product = Product.objects.get(name="My product 1")
        substitute = Product.objects.get(name="My product 2")
        response = self.client.get(
            "/save/" + str(product.id) + "/" + str(substitute.id),
            args=(product.id, substitute.id,),
            follow=True,
        )
        self.assertEquals(response.status_code, 200)

    def test_view(self):  # pragma: no cover
        product = Product.objects.get(name="My product 1")
        substitute = Product.objects.get(name="My product 2")
        response = self.client.get(
            reverse("substitute:save", args=(product.id, substitute.id,)), follow=True
        )
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "detail.html")

    def test_save(self):  # pragma: no cover
        product = Product.objects.get(name="My product 1")
        substitute = Product.objects.get(name="My product 2")
        response = self.client.get(
            reverse("substitute:save", args=(product.id, substitute.id,)), follow=True
        )
        product = response.context["product"]
        self.assertEqual(product.name, "My product 1")
        substitute = response.context["substitute"]
        self.assertEqual(substitute.name, "My product 2")
        self.assertTemplateUsed(response, "detail.html")
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Votre substitut a été sauvé")
        user = User.objects.get(username="testuser")
        self.assertTrue(
            Substitute.objects.filter(
                product_id=product, substitute_id=substitute, user_id=user
            ).exists()
        )


class DetailFavoritesTests(TestCase):
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
        self.credentials = {"username": "testuser", "password": "!!!!!!!!"}
        User.objects.create_user(**self.credentials)
        self.client.login(
            username=self.credentials["username"], password=self.credentials["password"]
        )
        product = Product.objects.get(name="My product 1")
        substitute = Product.objects.get(name="My product 2")
        user = User.objects.get(username="testuser")
        Substitute.objects.create(
            product_id=product, substitute_id=substitute, user_id=user
        )

    def test_DetailFavorites_page(self):  # pragma: no cover
        product = Product.objects.get(name="My product 1")
        substitute = Product.objects.get(name="My product 2")
        response = self.client.get(
            "/detail_favoris/" + str(product.id) + "/" + str(substitute.id),
            args=(product.id, substitute.id,),
            follow=True,
        )
        self.assertEquals(response.status_code, 200)

    def test_view(self):  # pragma: no cover
        product = Product.objects.get(name="My product 1")
        substitute = Product.objects.get(name="My product 2")
        response = self.client.get(
            reverse("substitute:detail_favoris", args=(product.id, substitute.id,)),
            follow=True,
        )
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "detail_favoris.html")

    def test_detail_favoris(self):  # pragma: no cover
        product = Product.objects.get(name="My product 1")
        substitute = Product.objects.get(name="My product 2")
        response = self.client.get(
            reverse("substitute:detail_favoris", args=(product.id, substitute.id,)),
            follow=True,
        )
        product = response.context["product"]
        self.assertEqual(product.name, "My product 1")
        substitute = response.context["substitute"]
        self.assertEqual(substitute.name, "My product 2")
        self.assertTemplateUsed(response, "detail_favoris.html")
