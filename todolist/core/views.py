from rest_framework import generics

from core.serializers import UserSerializer
from core.models import User


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
