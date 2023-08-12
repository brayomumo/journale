from rest_framework import serializers

from journale.journal.models import Journal


class JournalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Journal
        fields = ('__all__')