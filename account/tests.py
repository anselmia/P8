""" Account App Tests """
import os
from django.test import TestCase
from django.urls import reverse
from .models import User
from .forms import ConnexionForm, SignUpForm, UserUpdateForm
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()

# Create your tests here.
class LoginTests(TestCase):
    """ Unit Test Class for login function """

    def setUp(self):  # pragma: no cover
        """ Set Up of the test """
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
            reverse("account:login"),
            {"username": "testuser", "password": "!!!!!aaa"},
            follow=True,
        )
        self.assertFalse(response.context["user"].is_authenticated)

    def test_login(self):  # pragma: no cover
        response = self.client.post(
            reverse("account:login"), self.credentials, follow=True
        )
        self.assertTrue(response.context["user"].is_authenticated)

    def test_already_login(self):  # pragma: no cover
        self.client.login(
            username=self.credentials["username"], password=self.credentials["password"]
        )
        self.client.post(reverse("account:login"), self.credentials, follow=True)
        self.assertTemplateUsed("home.html")


class LoginLiveTestCase(LiveServerTestCase):
    """ Functional Test Class for login function """

    def setUp(self):  # pragma: no cover
        """ setUp of the test """
        self.credentials = {"username": "testuser", "password": "!!!!!!!!"}
        User.objects.create_user(**self.credentials)
        ChromeDriver = r"C:/Users/foxnono06/AppData/Local/chromedriver.exe"
        self.selenium = webdriver.Chrome(
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "chromedriver"),
            chrome_options=options,
        )
        super(LoginLiveTestCase, self).setUp()

    def tearDown(self):  # pragma: no cover
        """ Tear down of the test """
        self.selenium.quit()
        super(LoginLiveTestCase, self).tearDown()

    def test_login(self):  # pragma: no cover
        """ Simulate login action from webdriver """
        selenium = self.selenium
        # Opening the link we want to test
        selenium.get(f"{self.live_server_url}/login/")
        # find the form elements
        username = selenium.find_element_by_id("inputUsername")
        password = selenium.find_element_by_id("inputPassword")

        submit = selenium.find_element_by_name("submit")

        # # Fill the form with data
        username.send_keys("testuser")
        password.send_keys("!!!!!!!!")

        # # submitting the form
        submit.send_keys(Keys.RETURN)

        # check the returned result
        selenium.implicitly_wait(5)
        selenium.get(f"{self.live_server_url}")

        assert "  Se déconnecter" in selenium.page_source


class LogoutTests(TestCase):
    """ Unit Test Class for logout function """

    def setUp(self):  # pragma: no cover
        """ SetUp of the test """
        self.credentials = {"username": "testuser", "password": "!!!!!!!!"}
        User.objects.create_user(**self.credentials)

    def test_logout_page(self):  # pragma: no cover
        """ Test of logout view using verbal url """
        response = self.client.get("logout/")
        self.assertEquals(response.status_code, 404)

    def test_view(self):  # pragma: no cover
        """
        Test of logout view using reverse url
        """
        self.client.login(
            username=self.credentials["username"], password=self.credentials["password"]
        )
        response = self.client.get(reverse("account:logout"))
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse("home:index"))


class LogoutLiveTestCase(LiveServerTestCase):
    """ Functional Test Class for logout function """

    def setUp(self):  # pragma: no cover
        """ SetUp of the test """
        self.credentials = {
            "username": "usertest",
            "password": "!!!!!!!!",
            "email": "test_test@test.fr",
        }
        User.objects.create_user(**self.credentials)

        ChromeDriver = r"C:/Users/foxnono06/AppData/Local/chromedriver.exe"
        self.selenium = webdriver.Chrome()
        super(LogoutLiveTestCase, self).setUp()

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
        """ tearDown of the test """
        self.selenium.quit()
        super(LogoutLiveTestCase, self).tearDown()

    def test_logout(self):  # pragma: no cover
        """ Simulate logout action from webdriver """
        selenium = self.selenium
        # Opening the link we want to test
        selenium.get(f"{self.live_server_url}/profile/")
        selenium.maximize_window()
        selenium.implicitly_wait(5)
        logout = selenium.find_element_by_id("logout")
        logout.click()
        selenium.implicitly_wait(5)
        assert "Se connecter" in selenium.page_source
        current_url = selenium.current_url
        if (selenium.current_url[len(selenium.current_url) - 1]) == "/":
            current_url = selenium.current_url[:-1]
        assert current_url == f"{self.live_server_url}"


class RegisterTests(TestCase):
    """ Unit Test Class for register function """

    def setUp(self):  # pragma: no cover
        """ SetUp of the test """
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

    def test_SignUpForm_valid(self):  # pragma: no cover
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

    def test_SignUpForm_different_password(self):  # pragma: no cover
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

    def test_SignUpForm_invalid_password(self):  # pragma: no cover
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

    def test_SignUpForm_user_exist(self):  # pragma: no cover
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


class RegisterLiveTestCase(LiveServerTestCase):
    """ Functional Test Class for register function """

    def setUp(self):  # pragma: no cover
        """ SetUp of the test """
        ChromeDriver = r"C:/Users/foxnono06/AppData/Local/chromedriver.exe"
        self.selenium = webdriver.Chrome(executable_path=ChromeDriver)
        super(RegisterLiveTestCase, self).setUp()

    def tearDown(self):  # pragma: no cover
        """ tearDown of the test """
        self.selenium.quit()
        super(RegisterLiveTestCase, self).tearDown()

    def test_register(self):  # pragma: no cover
        """ Simulate register action from webdriver """
        selenium = self.selenium
        # Opening the link we want to test
        selenium.get(f"{self.live_server_url}/login/")
        selenium.maximize_window()
        selenium.implicitly_wait(5)

        register = selenium.find_element_by_id("register")
        register.click()
        wait = WebDriverWait(selenium, 20)
        wait.until(EC.visibility_of_element_located((By.ID, "id_robot")))
        selenium.maximize_window()

        username = selenium.find_element_by_id("id_username")
        email = selenium.find_element_by_id("id_email")
        password = selenium.find_element_by_id("id_password1")
        password2 = selenium.find_element_by_id("id_password2")
        robot = selenium.find_element_by_id("id_robot")
        submit = selenium.find_element_by_id("submit")

        i = 0
        while username.get_attribute("value") != "testuser" and i < 10:
            username.click()
            username.clear()
            username.send_keys("testuser")
            i += 1

        email.click()
        email.clear()
        email.send_keys("a@a.fr")
        password.click()
        password.clear()
        password.send_keys("!!!!!!!!")
        password2.click()
        password2.clear()
        password2.send_keys("!!!!!!!!")
        robot.click()
        submit.send_keys(Keys.RETURN)

        wait = WebDriverWait(selenium, 10)
        wait.until(EC.presence_of_element_located((By.ID, "search-button")))

        current_url = selenium.current_url
        if (selenium.current_url[len(selenium.current_url) - 1]) == "/":
            current_url = selenium.current_url[:-1]
        assert current_url == f"{self.live_server_url}"
        assert "  Se déconnecter" in selenium.page_source
        assert User.objects.filter(username="testuser").exists() is True


class ProfileTests(TestCase):
    """ Unit Test Class for profil function """

    def setUp(self):  # pragma: no cover
        """ SetUp of the test """
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

    def test_update_profile(self):  # pragma: no cover
        response = self.client.post(
            reverse("account:profile"),
            {"username": "user2", "email": "test@test.fr2"},
            follow=True,
        )
        # should be logged in now
        self.assertTrue(User.objects.filter(username="user2").exists())


class ProfileLiveTestCase(LiveServerTestCase):
    """ Functional Test Class for profile function """

    def setUp(self):  # pragma: no cover
        """ SetUp of the test """
        self.credentials = {
            "username": "usertest",
            "password": "!!!!!!!!",
            "email": "test_test@test.fr",
        }
        User.objects.create_user(**self.credentials)

        ChromeDriver = r"C:/Users/foxnono06/AppData/Local/chromedriver.exe"
        self.selenium = webdriver.Chrome(executable_path=ChromeDriver)
        super(ProfileLiveTestCase, self).setUp()

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
        """ tearDown of the test """
        self.selenium.quit()
        super(ProfileLiveTestCase, self).tearDown()

    def test_profile(self):  # pragma: no cover
        """ Simulate profile visite action from webdriver """
        selenium = self.selenium
        selenium.get(f"{self.live_server_url}")
        selenium.maximize_window()
        selenium.implicitly_wait(5)

        profile = selenium.find_element_by_id("profile")
        profile.click()
        wait = WebDriverWait(selenium, 20)
        wait.until(EC.visibility_of_element_located((By.NAME, "confirm_change")))
        selenium.maximize_window()

        username = selenium.find_element_by_id("id_username")
        submit = selenium.find_element_by_name("confirm_change")
        selenium.execute_script(
            "document.querySelector('button.disabled').removeAttribute('disabled')"
        )
        selenium.execute_script(
            "document.querySelector('button.disabled').classList.remove('disabled')"
        )

        i = 0
        while username.get_attribute("value") != "testuser" and i < 10:
            username.click()
            username.clear()
            username.send_keys("testuser")
            i += 1

        submit.send_keys(Keys.RETURN)
        assert (
            "Les modifications de votre profil ont bien été enregistrées"
            in selenium.page_source
        )
        assert User.objects.filter(username="testuser").exists() is True


class FavoritesTests(TestCase):
    """ Unit Test Class for profil function """

    def setUp(self):  # pragma: no cover
        """ SetUp of the test """
        self.credentials = {
            "username": "usertest",
            "password": "!!!!!!!!",
            "email": "test_test@test.fr",
        }
        User.objects.create_user(**self.credentials)
        self.client.login(
            username=self.credentials["username"], password=self.credentials["password"]
        )

    def test_favorites_page(self):  # pragma: no cover
        """ Test of favorites view using verbal url """
        response = self.client.get("/favorites/")
        self.assertEquals(response.status_code, 200)

    def test_view(self):  # pragma: no cover
        """
        Test of favorites view using reverse url
        assert http redirect code
        assert used template is favorite.html
        assert favorites exist in contect
        """
        response = self.client.get(reverse("account:favorites"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "favorites.html")
        self.assertIsNotNone(response.context["favoris"])


class FavoriteLiveTestCase(LiveServerTestCase):
    """ Unit Test Class for favorite function """

    def setUp(self):  # pragma: no cover
        """ SetUp of the test """
        self.credentials = {
            "username": "usertest",
            "password": "!!!!!!!!",
            "email": "test_test@test.fr",
        }
        User.objects.create_user(**self.credentials)

        ChromeDriver = r"C:/Users/foxnono06/AppData/Local/chromedriver.exe"
        self.selenium = webdriver.Chrome(executable_path=ChromeDriver)
        super(FavoriteLiveTestCase, self).setUp()

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
        super(FavoriteLiveTestCase, self).tearDown()

    def test_favorite(self):  # pragma: no cover
        selenium = self.selenium
        selenium.get(f"{self.live_server_url}")
        selenium.maximize_window()
        selenium.implicitly_wait(5)

        favorites = selenium.find_element_by_id("favorites")
        favorites.click()
        wait = WebDriverWait(selenium, 20)
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "table")))
        selenium.maximize_window()

        assert "Mes Favoris" in selenium.page_source
