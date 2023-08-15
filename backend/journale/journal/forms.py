from typing import Any
from django import forms

from journale.journal.models import Journal


class JournalForm(forms.ModelForm):
    class Meta:
        model = Journal
        fields = ("title", "text")
