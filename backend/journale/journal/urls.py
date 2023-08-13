from django.urls import path, include
from rest_framework.routers import DefaultRouter


from journale.journal.views import JournalViewset, get_journals, create_journal, update_journal

journalRouter  = DefaultRouter()
journalRouter.register("", JournalViewset, basename="journals")

urlpatterns = [
    path("",get_journals, name="journals"),
    path("new", create_journal, name="create-journal"),
    path("update/<int:id>", update_journal, name="update-journal")
]