from django.test import TestCase

from model_bakery import baker
from journale.journal.models import Journal


class TestJournal(TestCase):
    def test_create_journal(self):
        journal = baker.make(
            Journal, title="Test thought", text="This is a very random test thought"
        )
        # get journal
        journ = Journal.objects.all()
        journ_24 = Journal.last_24_hrs()
        self.assertEqual(journ.count(), 1)
        self.assertEqual(journ.first().title, "Test thought")
        self.assertEqual(journ_24.count(), journ.count())

    def test_update_journal(self):
        journal = baker.make(Journal, title="Life is lifing")
        journal = Journal.objects.first()
        self.assertEqual(journal.title, "Life is lifing")

        journal.title = "Updated Thought"
        journal.save()
        journal.refresh_from_db()
        self.assertEqual(journal.title, "Updated Thought")

    def test_delete_journal(self):
        baker.make(Journal)

        journals = Journal.objects.all()
        self.assertEqual(journals.count(), 1)
        journ = journals.first()
        journ.delete()
        journals = Journal.objects.all()
        self.assertNotEqual(journals.count(), 1)
