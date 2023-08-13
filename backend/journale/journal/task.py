import random
from django.core.mail import send_mail
from django.conf import settings

from journale.journal.models import Journal
from journale.wenyeji.models import User



def get_random_journal(journals, user_id):
    user = User.objects.get(id=user_id)
    index = random.randint(0, journals.count())
    journ = journals[index]
    if journ.owner == user:
        return get_random_journal(journals, user_id)
    else:
        return user, journ


def send_journals():
    journals = Journal.last_24_hrs()
    users = set(journals.values_list("owner", flat=True))
    for user in users:
        u, journal = get_random_journal(journals, user)
        send_mail(
            "Daily Random Journal",
            journal.text,
            settings.EMAIL_HOST_USER,
            [u.email]
        )