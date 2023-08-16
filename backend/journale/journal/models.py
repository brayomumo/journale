from django.db import models
from django.conf import settings
from django.utils import timezone

from journale.common.models import BaseModel


class Journal(BaseModel):
    title = models.CharField(max_length=200)
    text = models.TextField()
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="journal_owner", on_delete=models.PROTECT
    )

    @classmethod
    def last_24_hrs(cls):
        """
        This is a class method used to get all Journals created in the last 24hrs.
        """
        last_24hrs = timezone.now() - timezone.timedelta(hours=24)
        return cls.objects.filter(created__gte=last_24hrs)
