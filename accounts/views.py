from django.contrib.auth import get_user_model
from rest_framework import generics, viewsets
from accounts.serializers import UserSerializer
from rest_framework.permissions import IsAdminUser
from django.views.generic import CreateView
from accounts.forms import CustomUserCreationForm
from django.urls import reverse_lazy

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

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('accounts:login')
    template_name = "registration/signup.html" 