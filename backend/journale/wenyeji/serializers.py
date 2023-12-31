from rest_framework import serializers

from journale.wenyeji.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model  = User
        fields = ("id", "username", "first_name", "last_name","email", "created", "updated")