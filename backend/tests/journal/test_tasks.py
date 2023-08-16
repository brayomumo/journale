from unittest import mock
from django.test import TestCase
from model_bakery import baker

from django.core import mail

from journale.journal.models import Journal
from journale.journal.task import send_journals, get_random_journal


class TestJournalTask(TestCase):
    def setUp(self):
        self.journals = baker.make(Journal, _quantity=10)
        assert Journal.objects.count() == 10

    def test_get_random_journal(self):
        journals = Journal.last_24_hrs()
        users = set(journals.values_list("owner", flat=True))
        user, _ = get_random_journal(journals, list(users)[0])
        self.assertEqual(user.id, list(users)[0])

    def test_send_journals(self):
        send_journals()
        self.assertEqual(len(mail.outbox), 10)

    def test_task_edge_cases(self):
        journals = Journal.last_24_hrs()
        users = set(journals.values_list("owner", flat=True))
        user, journal = get_random_journal(journals, list(users)[0], retries=6)
        self.assertIsNone(user)
        self.assertIsNone(journal)

        with mock.patch("journale.journal.task.get_random_journal") as mock_shuffle:
            mock_shuffle.return_value = (None, None)
            with mock.patch("journale.journal.task.send_mail") as mock_mailer:
                send_journals()
                mock_mailer.assert_not_called()
