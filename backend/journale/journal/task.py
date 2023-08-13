from journale.journal.models import Journal



def send_journals():
    journals = Journal.last_24_hrs()
    users = journals.values_list("owner")
    print(journals.count(), users.count())