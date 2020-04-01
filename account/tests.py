from django.test import TestCase
from django.urls import reverse
from .models import User
from django.contrib.auth import authenticate, login as auth_login
from .forms import ConnexionForm, SignUpForm, UserUpdateForm
from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from unittest.mock import patch


# Create your tests here.
class LoginTests(TestCase):
    def setUp(self):  # pragma: no cover
        self.credentials = {"username": "testuser", "password": "!!!!!!!!"}
        User.objects.create_user(**self.credentials)

    def test_login_page(self):  # pragma: no cover
        response = self.client.get("/login/")
        self.assertEquals(response.status_code, 200)

    def test_view(self):  # pragma: no cover
        response = self.client.get(reverse("account:login"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")

    def test_UserForm_valid(self):  # pragma: no cover
        form = ConnexionForm(data={"username": "user", "password": "user"})
        self.assertTrue(form.is_valid())

    def test_UserForm_invalid(self):  # pragma: no cover
        form = ConnexionForm(data={"username": "user"})
        self.assertFalse(form.is_valid())

    def test_invalid_login(self):  # pragma: no cover
        response = self.client.post(
            reverse("account:login"), {"username": "testuser", "password": "!!!!!aaa"}, follow=True
        )
        # should be logged in now
        self.assertFalse(response.context["user"].is_authenticated)

    def test_login(self):  # pragma: no cover
        response = self.client.post(
            reverse("account:login"), self.credentials, follow=True
        )
        # should be logged in now

        self.assertTrue(response.context["user"].is_authenticated)

    def test_already_login(self):  # pragma: no cover
        self.client.login(
            username=self.credentials["username"], password=self.credentials["password"]
        )
        self.client.post(
            reverse("account:login"), self.credentials, follow=True
        )
        # should be logged in now
        self.assertTemplateUsed('home.html')


class LoginTestCase(StaticLiveServerTestCase):

    def setUp(self):  # pragma: no cover
        ChromeDriver = r"C:/Users/foxnono06/AppData/Local/chromedriver.exe"
        self.selenium = webdriver.Chrome(executable_path=ChromeDriver)
        super(LoginTestCase, self).setUp()

    def tearDown(self):  # pragma: no cover
        self.selenium.quit()
        super(LoginTestCase, self).tearDown()

    def test_register(self):  # pragma: no cover
        selenium = self.selenium
        # Opening the link we want to test
        selenium.get('127.0.0.1:8000/login')
        # find the form element
        username = selenium.find_element_by_id('inputUsername')
        password = selenium.find_element_by_id('inputPassword')

        submit = selenium.find_element_by_name('register')

        # Fill the form with data
        username.send_keys('aa')
        password.send_keys('!!!!!!!!')

        # submitting the form
        submit.send_keys(Keys.RETURN)

        # check the returned result
        assert 'Check your email' in selenium.page_source


class LogoutTests(TestCase):
    def setUp(self):  # pragma: no cover
        self.credentials = {"username": "testuser", "password": "!!!!!!!!"}
        User.objects.create_user(**self.credentials)

    def test_logout_page(self):  # pragma: no cover
        response = self.client.get("logout/")
        self.assertEquals(response.status_code, 404)

    def test_view(self):  # pragma: no cover
        self.client.login(
            username=self.credentials["username"], password=self.credentials["password"]
        )
        response = self.client.get(reverse("account:logout"))
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse("home:index"))


class RegisterTests(TestCase):
    def setUp(self):  # pragma: no cover
        self.credentials = {
            "username": "usertest",
            "email": "test_test@test.fr",
            "password": "!!!!!!!!",
        }

    def test_register_page(self):  # pragma: no cover
        response = self.client.get("/register/")
        self.assertEquals(response.status_code, 200)

    def test_view(self):  # pragma: no cover
        response = self.client.get(reverse("account:register"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "register.html")

    def test_RegisterForm_valid(self):  # pragma: no cover
        form = SignUpForm(
            data={
                "username": "user1",
                "email": "test@test.fr1",
                "password1": "!!!!!!!!",
                "password2": "!!!!!!!!",
                "robot": True,
            }
        )
        self.assertTrue(form.is_valid())

    def test_RegisterForm_different_password(self):  # pragma: no cover
        form = SignUpForm(
            data={
                "username": "user",
                "email": "test@test.fr",
                "password1": "!!!!!!!!",
                "password2": "!!!!!!!a",
                "robot": True,
            }
        )
        self.assertFalse(form.is_valid())

    def test_RegisterForm_invalid_password(self):  # pragma: no cover
        form = SignUpForm(
            data={
                "username": "user",
                "email": "test@test.fr",
                "password1": "aaaaaaaa",
                "password2": "aaaaaaaa",
                "robot": True,
            }
        )
        self.assertFalse(form.is_valid())

    def test_RegisterForm_user_exist(self):  # pragma: no cover
        User.objects.create_user(**self.credentials)
        form = SignUpForm(
            data={
                "username": "usertest",
                "email": "test_test@test.f",
                "password1": "!!!!!!!!",
                "password2": "!!!!!!!!",
                "robot": True,
            }
        )
        self.assertFalse(form.is_valid())

    def test_register(self):  # pragma: no cover
        response = self.client.post(
            reverse("account:register"),
            {
                "username": "user2",
                "email": "test@test.fr2",
                "password1": "!!!!!!!!",
                "password2": "!!!!!!!!",
                "robot": True,
            },
            follow=True,
        )
        # should be logged in now
        self.assertTrue(User.objects.filter(username="user2").exists())


class ProfilTests(TestCase):
    def setUp(self):  # pragma: no cover
        self.credentials = {
            "username": "usertest",
            "password": "!!!!!!!!",
            "email": "test_test@test.fr",
        }
        User.objects.create_user(
            username="usertest2", password="!!!!!!!!", email="test_test@test2.fr"
        )
        User.objects.create_user(**self.credentials)
        self.client.login(
            username=self.credentials["username"], password=self.credentials["password"]
        )
        self.user = User.objects.get(username=self.credentials["username"])

    def test_profile_page(self):  # pragma: no cover
        response = self.client.get("/profile/")
        self.assertEquals(response.status_code, 200)

    def test_view(self):  # pragma: no cover
        response = self.client.get(reverse("account:profile"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "profile.html")

    def test_UserUpdateForm_valid(self):  # pragma: no cover

        form = UserUpdateForm(
            data={"username": "user1", "email": "test@test.fr1"}, instance=self.user
        )
        self.assertTrue(form.is_valid())

    def test_UserUpdateForm_invalid_user_exist(self):  # pragma: no cover
        form = UserUpdateForm(
            data={"user_name": "usertest2", "email": "test@test.fr2222"},
            instance=self.user,
        )
        self.assertFalse(form.is_valid())

    def test_UserUpdateForm_invalid_email_exist(self):  # pragma: no cover
        form = UserUpdateForm(
            data={"user_name": "user", "email": "test_test@test2.fr"},
            instance=self.user,
        )
        self.assertFalse(form.is_valid())

    def test_update_profil(self):  # pragma: no cover
        response = self.client.post(
            reverse("account:profile"),
            {"username": "user2", "email": "test@test.fr2"},
            follow=True,
        )
        # should be logged in now
        self.assertTrue(User.objects.filter(username="user2").exists())


class FavoritesTests(TestCase):
    def setUp(self):  # pragma: no cover
        self.credentials = {
            "username": "usertest",
            "password": "!!!!!!!!",
            "email": "test_test@test.fr",
        }
        User.objects.create_user(**self.credentials)
        self.client.login(
            username=self.credentials["username"], password=self.credentials["password"]
        )
        self.user = User.objects.get(username=self.credentials["username"])

    def test_favorites_page(self):  # pragma: no cover
        response = self.client.get("/favorites/")
        self.assertEquals(response.status_code, 200)

    def test_view(self):  # pragma: no cover
        response = self.client.get(reverse("account:favorites"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "favorites.html")
        self.assertIsNotNone(response.context["favoris"])
