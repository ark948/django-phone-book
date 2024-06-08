from django.contrib.auth import get_user_model
from django.http import HttpRequest, HttpResponse
from rest_framework import generics, viewsets
from accounts.serializers import UserSerializer
from rest_framework.permissions import IsAdminUser
from django.views.generic import CreateView
from accounts.forms import CustomUserCreationForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView

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

    def get(self, request: HttpRequest, *args: str, **kwargs: reverse_lazy) -> HttpResponse:
        if request.user.is_authenticated:
            messages.info(request, "شما وارد سایت شده اید.")
            return redirect("pages:index")
        return super().get(request, *args, **kwargs)
    
class CustomLoginView(LoginView):

    def get(self, request: HttpRequest, *args: str, **kwargs: reverse_lazy) -> HttpResponse:
        if request.user.is_authenticated:
            messages.info(request, "شما وارد سایت شده اید.")
            return redirect("pages:index")
        return super().get(request, *args, **kwargs)
    
    def get_success_url(self) -> str:
        messages.success(self.request, "با موفقیت وارد سایت شدید.")
        return super().get_success_url()