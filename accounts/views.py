from django.contrib.auth import get_user_model
from rest_framework import generics, viewsets
from accounts.serializers import UserSerializer
from rest_framework.permissions import IsAdminUser

class UserList(generics.ListCreateAPIView):
    permission_classes = (IsAdminUser,)
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer