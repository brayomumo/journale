import json
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from journale.journal.models import Journal
from journale.journal.serilizers import JournalSerializer


class JournalViewset(viewsets.ModelViewSet):
    queryset = Journal.objects.all()
    serializer_class = JournalSerializer

    # def create(self, request, *args, **kwargs):
    #     payload = request.data
    #     owner_id = request.data.get("owner")
    #     owner = get_user_model().objects.get(id=owner_id)
    #     payload['owner_id'] = owner_id
    #     serializer = JournalSerializer(data=payload)

    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

