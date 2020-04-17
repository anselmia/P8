from django.test import TestCase
from unittest.mock import patch
from django.urls import reverse
from account.models import User
from home.models import Product, Category
from .models import Substitute
from django.contrib.messages import get_messages
from django.test import LiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

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


class SubstituteLiveTestCase(LiveServerTestCase):
    def setUp(self):  # pragma: no cover
        self.selenium = webdriver.Chrome()
        super(SubstituteLiveTestCase, self).setUp()
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

    def tearDown(self):  # pragma: no cover
        self.selenium.quit()
        super(SubstituteLiveTestCase, self).tearDown()

    def test_substitute(self):  # pragma: no cover
        selenium = self.selenium
        product = Product.objects.get(name="My product 1")
        selenium.get(f"{self.live_server_url}")
        selenium.maximize_window()
        selenium.implicitly_wait(5)

        text = selenium.find_element_by_class_name("main-search")
        submit = selenium.find_element_by_id("search-button")
        text.send_keys("product")
        submit.click()
        wait = WebDriverWait(selenium, 20)
        wait.until(EC.url_to_be(f"{self.live_server_url}/product/"))

        product_1 = selenium.find_element_by_xpath(
            f"//a[@href='/substitute/{product.id}']"
        )
        while selenium.current_url == f"{self.live_server_url}/product/":
            product_1.click()

        wait = WebDriverWait(selenium, 20)
        wait.until(EC.url_to_be(f"{self.live_server_url}/substitute/{product.id}"))

        current_url = selenium.current_url
        if (selenium.current_url[len(selenium.current_url) - 1]) == "/":
            current_url = selenium.current_url[:-1]

        assert current_url == f"{self.live_server_url}/substitute/{str(product.id)}"
        assert selenium.find_element_by_xpath("//a[@href='?page=2']") is not None
        assert "Résultat de la recherche pour :" in selenium.page_source


class DetailTests(TestCase):
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
        substitute = response.context["substitute"]
        self.assertEqual(substitute.name, "My product 2")
        self.assertTemplateUsed(response, "detail.html")
        self.assertFalse(response.context["exist"])

    def test_detail_favoris_exist(self):  # pragma: no cover
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


class DetailLiveTestCase(LiveServerTestCase):
    def setUp(self):  # pragma: no cover
        self.selenium = webdriver.Chrome()
        super(DetailLiveTestCase, self).setUp()
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

    def tearDown(self):  # pragma: no cover
        self.selenium.quit()
        super(DetailLiveTestCase, self).tearDown()

    def test_detail(self):  # pragma: no cover
        selenium = self.selenium
        product = Product.objects.get(name="My product 1")
        substitute = Product.objects.get(name="My product 2")
        find_url = f"{reverse('substitute:search-a-substitute', kwargs={'product_id':product.id})}"
        selenium.get(self.live_server_url + find_url)
        selenium.maximize_window()
        selenium.implicitly_wait(5)

        substitute_a = selenium.find_element_by_xpath(
            f"//a[@href='/detail/{product.id}/{substitute.id}/']"
        )
        while (
            selenium.current_url
            == f"{self.live_server_url}/substitute/{str(product.id)}"
        ):
            substitute_a.click()

        current_url = selenium.current_url
        if (selenium.current_url[len(selenium.current_url) - 1]) == "/":
            current_url = selenium.current_url[:-1]

        assert (
            current_url
            == f"{self.live_server_url}/detail/{str(product.id)}/{str(substitute.id)}"
        )
        assert "Voir La Fiche d'OpenFoodFacts" in selenium.page_source
        assert (
            "Vous devez vous connecter pour enregistrer ce substitut"
            in selenium.page_source
        )


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
        self.assertEqual(str(messages[0]), "Votre substitut a été sauvé")
        user = User.objects.get(username="testuser")
        self.assertTrue(
            Substitute.objects.filter(
                product_id=product, substitute_id=substitute, user_id=user
            ).exists()
        )


class SaveLiveTestCase(LiveServerTestCase):
    def setUp(self):  # pragma: no cover
        self.credentials = {
            "username": "usertest",
            "password": "!!!!!!!!",
            "email": "test_test@test.fr",
        }
        User.objects.create_user(**self.credentials)
        self.selenium = webdriver.Chrome()
        super(SaveLiveTestCase, self).setUp()
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

        # Login the user
        self.assertTrue(
            self.client.login(
                username=self.credentials["username"],
                password=self.credentials["password"],
            )
        )
        # Add cookie to log in the browser
        cookie = self.client.cookies["sessionid"]
        self.selenium.get(
            self.live_server_url
        )  # visit page in the site domain so the page accepts the cookie
        self.selenium.add_cookie(
            {"name": "sessionid", "value": cookie.value, "secure": False, "path": "/"}
        )

    def tearDown(self):  # pragma: no cover
        self.selenium.quit()
        super(SaveLiveTestCase, self).tearDown()

    def test_save(self):  # pragma: no cover
        selenium = self.selenium
        product = Product.objects.get(name="My product 1")
        substitute = Product.objects.get(name="My product 2")
        find_url = f"{reverse('substitute:detail',kwargs={'product_id':product.id, 'substitute_id':substitute.id})}"
        selenium.get(self.live_server_url + find_url)
        selenium.maximize_window()
        selenium.implicitly_wait(5)

        save = selenium.find_element_by_xpath(
            f"//a[@href='/save/{product.id}/{substitute.id}/']"
        )
        save.click()
        current_url = selenium.current_url
        if (selenium.current_url[len(selenium.current_url) - 1]) == "/":
            current_url = selenium.current_url[:-1]

        assert (
            current_url
            == f"{self.live_server_url}/save/{str(product.id)}/{str(substitute.id)}"
        )
        assert "Votre substitut a été sauvé" in selenium.page_source
        user = User.objects.get(username="usertest")
        assert Substitute.objects.filter(
            product_id=product, substitute_id=substitute, user_id=user
        ).exists()


class DetailFavorisTests(TestCase):
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

    def test_DetailFavoris_page(self):  # pragma: no cover
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


class DetailFavorisLiveTestCase(LiveServerTestCase):
    def setUp(self):  # pragma: no cover
        self.credentials = {
            "username": "usertest",
            "password": "!!!!!!!!",
            "email": "test_test@test.fr",
        }
        User.objects.create_user(**self.credentials)
        self.selenium = webdriver.Chrome()
        super(DetailFavorisLiveTestCase, self).setUp()
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

        product = Product.objects.get(name="My product 1")
        substitute = Product.objects.get(name="My product 2")
        user = User.objects.get(username="usertest")
        Substitute.objects.create(
            product_id=product, substitute_id=substitute, user_id=user
        )
        # Login the user
        self.assertTrue(
            self.client.login(
                username=self.credentials["username"],
                password=self.credentials["password"],
            )
        )
        # Add cookie to log in the browser
        cookie = self.client.cookies["sessionid"]
        self.selenium.get(
            self.live_server_url
        )  # visit page in the site domain so the page accepts the cookie
        self.selenium.add_cookie(
            {"name": "sessionid", "value": cookie.value, "secure": False, "path": "/"}
        )

    def tearDown(self):  # pragma: no cover
        self.selenium.quit()
        super(DetailFavorisLiveTestCase, self).tearDown()

    def test_save(self):  # pragma: no cover
        selenium = self.selenium
        product = Product.objects.get(name="My product 1")
        substitute = Product.objects.get(name="My product 2")
        selenium.get(f"{self.live_server_url}/favorites")
        selenium.maximize_window()
        selenium.implicitly_wait(5)

        details_favoris = selenium.find_element_by_xpath(
            f"//a[@href='/detail_favoris/{product.id}/{substitute.id}/']"
        )
        while selenium.current_url == f"{self.live_server_url}/favorites/":
            details_favoris.click()
        current_url = selenium.current_url
        if (selenium.current_url[len(selenium.current_url) - 1]) == "/":
            current_url = selenium.current_url[:-1]

        assert (
            current_url
            == f"{self.live_server_url}/detail_favoris/{str(product.id)}/{str(substitute.id)}"
        )
        assert "Détails du favoris" in selenium.page_source
