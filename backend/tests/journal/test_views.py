from django.test import TestCase
from unittest import mock
from model_bakery import baker

from journale.wenyeji.models import User
from journale.journal.forms import JournalForm
from journale.journal.models import Journal
from journale.journal.views import create_journal, update_journal, get_journals


class TestJournalViews(TestCase):
    def setUp(self):
        baker.make(Journal, _quantity=10)
        return super().setUp()

    def login(self):
        """Helper function to authenticate,
        returns True if login was successful
        return False if credentials don't match.
        """
        self.user = User.objects.create_user(
            "testUser", "test.user@mail.com", "1X<ISRUkw+tuK"
        )
        return self.client.login(username="testUser", password="1X<ISRUkw+tuK")

    def test_get_journals_unauthenticated(self):
        def asserter(response):
            """Inner function to avoid re-writing same asserts"""
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.url, "/users/login")

        response = self.client.get("/")
        asserter(response)

        response = self.client.post("/new")
        asserter(response)

        response = self.client.put("/update/1")
        asserter(response)

    def test_get_journals(self):
        login = self.login()
        self.assertTrue(login)

        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["count"], 0)

        baker.make(Journal, owner=self.user)
        journs = Journal.objects.filter(owner__id=self.user.id)
        assert journs.count() == 1

        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["count"], 1)
        self.assertTemplateUsed(response, "home.html")

    @mock.patch("journale.journal.views.messages")
    def test_create_journal(self, mock_messages):
        login = self.login()
        self.assertTrue(login)

        response = self.client.get("/new")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "journal/new_journal.html")
        journal = {
            "title": "Random thought",
            "text": "This is the most random thought ever tested",
        }
        response = self.client.post("/new", journal)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")
        journals = Journal.objects.filter(owner__id=self.user.id)
        assert journals.count() == 1
        call = mock_messages.success.call_args
        self.assertEqual(call.args[1], "Journal created successfully.")

    @mock.patch("journale.journal.views.messages")
    def test_update_journal(self, mock_messages):
        login = self.login()
        self.assertTrue(login)

        journal = baker.make(Journal, owner=self.user)
        url = f"/update/{journal.id}"
        response = self.client.get(url)
        self.assertTemplateUsed(response, "journal/update_journal.html")

        response = self.client.post(
            url, {"title": "This is new title", "text": journal.text}
        )
        assert response.status_code == 302
        assert response.url == "/"
        call = mock_messages.success.call_args
        self.assertEqual(call.args[1], "Journal Updated successfully.")

    def test_update_404_journal(self):
        login = self.login()
        self.assertTrue(login)

        response = self.client.post(
            "update/10",
            {"titler": "This is new title", "text": "Invalid thoughts, need help"},
        )
        assert response.status_code == 404
        self.assertTemplateUsed(response, "404.html")

    @mock.patch("journale.journal.views.messages")
    def test_Journaling_with_invalid_data(self, mock_messages):
        login = self.login()
        self.assertTrue(login)

        journal = {
            "titler": "Random thought",
            "text": "This is the most random thought ever tested",
        }
        response = self.client.post("/new", journal)
        self.assertEqual(response.status_code, 200)
        mock_messages.success.assert_not_called()
        call = mock_messages.error.call_args
        self.assertEqual(call.args[1], "Error saving Journal!")

        # Error updating Journal
        journal = baker.make(Journal, owner=self.user)
        url = f"/update/{journal.id}"

        response = self.client.post(
            url, {"titler": "This is new title", "text": journal.text}
        )
        assert response.status_code == 200
        call = mock_messages.error.call_args
        self.assertEqual(call.args[1], "Error Updating Journal!")


class TestJournalForm(TestCase):
    def test_create_JournalForm(self):
        # create journal
        form = JournalForm()
        self.assertTrue(form.fields["title"].label is not None)
        self.assertTrue(form.fields["text"].label is not None)

        form = JournalForm(
            data={
                "title": "Test Title",
                "text": "This is a random test thought",
                "owner_id": 1,
            }
        )
        self.assertTrue(form.is_valid())

    def test_JournalForm_is_invalid(self):
        form = JournalForm(
            data={
                "titler": "Test Title",
                "text": "This is a random test thought",
                "owner_id": 1,
            }
        )

        self.assertFalse(form.is_valid())
