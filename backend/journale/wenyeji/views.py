from rest_framework import viewsets

from journale.wenyeji.models import User
from journale.wenyeji.serializers import UserSerializer

# Create your views here.
class UserViewset(viewsets.ModelViewSet):
    queryset  = User.objects.all()
    serializer_class = UserSerializer
