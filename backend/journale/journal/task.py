import random
from django.core.mail import send_mail
from django.conf import settings

from journale.journal.models import Journal
from journale.wenyeji.models import User



def get_random_journal(journals, user_id, retries = 0):
    """
    Get random journal for a user.It recursively searches for journal to be
    send to a user. Max retries is 5.

    Args:
        journals: Queryset - List for all journals in the last 24hrs
        user_id: int - Id for the user to be sent a random journal
        retries: int - Count of how many retries when getting a journal
                for user
    """
    if retries > 5:
        return None, None
    user = User.objects.get(id=user_id)
    index = random.randint(0, journals.count()-1)
    journ = journals[index]
    if journ.owner == user:
        return get_random_journal(journals, user_id, retries=retries+1)
    else:
        return user, journ


def send_journals():
    """
    Gets all Journals created in the last 24hrs and users and shuffles the users
    to journal, then sends the shuffled journal to the user.
    """
    journals = Journal.last_24_hrs()
    users = set(journals.values_list("owner", flat=True))
    if journals.count() < 1 or len(users) < 1:
        return

    for user in users:
        u, journal = get_random_journal(journals, user)
        if u is None and journal is None:
            continue
        send_mail(
            "Daily Random Journal",
            journal.text,
            settings.EMAIL_HOST_USER,
            [u.email]
        )