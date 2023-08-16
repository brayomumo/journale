from django.test import TestCase
from model_bakery import baker
from unittest import mock

from journale.wenyeji.models import User
from journale.wenyeji.views import user_register, user_login, user_logout
from journale.wenyeji.forms import NewUserForm


class TestUserViews(TestCase):
    @mock.patch("journale.wenyeji.views.messages")
    def test_create_user(self, mock_messages):
        response = self.client.get("/users/register")
        assert response.status_code == 200
        self.assertTemplateUsed(response, "users/register.html")

        response = self.client.post(
            "/users/register",
            {
                "username": "testUser",
                "email": "test.user@mail.com",
                "password1": "X<ISRUkw+tuK",
                "password2": "X<ISRUkw+tuK",
            },
        )
        assert response.status_code == 302
        call = mock_messages.success.call_args
        self.assertEqual(call.args[1], "Registration successful.")

    @mock.patch("journale.wenyeji.views.messages")
    def test_invalid_user_registration(self, mock_messages):
        response = self.client.post(
            "/users/register",
            {
                "username": "testUser",
                "password1": "X<ISRUkw+tuK",
                "password2": "X<ISRUkw+tuK",
            },
        )
        mock_messages.success.assert_not_called()
        call = mock_messages.error.call_args
        self.assertEqual(
            call.args[1], "Unsuccessful registration. Invalid information."
        )

    @mock.patch("journale.wenyeji.views.messages")
    def test_user_login(self, mock_messages):
        User.objects.create_user(
            username="testUser", email="test.user@mail.com", password="X<ISRUkw+tuK"
        )

        response = self.client.get("/users/login")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/login.html")

        # Test actual thing
        response = self.client.post(
            "/users/login", {"username": "testUser", "password": "X<ISRUkw+tuK"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")
        call = mock_messages.info.call_args
        self.assertEqual(call.args[1], "You are now logged in as testUser.")

        # Test wierd form submission
        response = self.client.post(
            "/users/login", {"usern-jina": "testUser", "password": "X<ISRUkw+tuK"}
        )
        self.assertEqual(response.status_code, 200)
        call = mock_messages.error.call_args
        self.assertEqual(call.args[1], "Invalid username or password.")

        # Test invalid login
        with mock.patch("journale.wenyeji.views.authenticate") as mock_authenticate:
            mock_authenticate.return_value = None
            response = self.client.post(
                "/users/login", {"username": "testUser", "password": "X<ISRUkw+tuK"}
            )
            call = mock_messages.error.call_args
            self.assertEqual(call.args[1], "Invalid username or password.")
            self.assertEqual(response.status_code, 200)

    @mock.patch("journale.wenyeji.views.messages")
    def test_user_logout(self, mock_messages):
        response = self.client.get("/users/logout")

        assert response.status_code == 302
        assert response.url == "/"
        call = mock_messages.info.call_args
        self.assertEqual(call.args[1], "You have successfully logged out.")


class TestUserForm(TestCase):
    def test_create_new_user(self):
        form = NewUserForm()
        self.assertTrue(form.fields["username"].label is not None)
        self.assertTrue(form.fields["password1"].label is not None)
        self.assertTrue(form.fields["password2"].label is not None)

        form = NewUserForm(
            data={
                "username": "NewUser",
                "email": "new.user@mail.com",
                "password1": "anotherPassWord",
                "password2": "anotherPassWord",
            }
        )
        self.assertTrue(form.is_valid())
        user = form.save(commit=True)
        self.assertEqual(user.username, "NewUser")

    def test_invalid_form(self):
        form = NewUserForm(data={"username": "NewUser", "password": "anotherPassWord"})
        self.assertFalse(form.is_valid())
