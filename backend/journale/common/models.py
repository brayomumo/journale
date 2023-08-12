from django.db import models

# Create your models here.
class BaseModel(models.Model):
    created = models.DateTimeField(auto_now=True)
    updated = models.DateField(auto_now=True)


    class Meta:
        abstract = True
        ordering = ['-created', '-updated']
