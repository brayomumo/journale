from django.urls import path, include
from rest_framework.routers import DefaultRouter


from journale.journal.views import JournalViewset

journalRouter  = DefaultRouter()
journalRouter.register("", JournalViewset, basename="journals")

# urlpatterns = [
#     path("", include(journalRouter))
# ]