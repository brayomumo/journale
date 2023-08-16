from django.test import TestCase
from model_bakery import baker
from django.db.utils import IntegrityError

from journale.wenyeji.models import User


class TestUserModel(TestCase):
    def test_create_user(self):
        user = baker.make(User, username="testUser", email="test.user@mail")
        count = User.objects.count()

        assert count == 1
        assert user.id is not None

    def test_update_user(self):
        user = baker.make(User, username="TestUser")
        assert User.objects.count() == 1

        assert user.username == "TestUser"
        user.username = "TestUpdate"
        user.save()
        user.refresh_from_db()
        assert user.username == "TestUpdate"
