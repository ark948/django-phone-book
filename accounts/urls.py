from django.urls import path
from accounts.views import UserList, UserDetail, UserViewSet, SignUpView, CustomLoginView
from rest_framework.routers import SimpleRouter
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'accounts'

router = SimpleRouter()
router.register(r"users", UserViewSet)

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path("login/", CustomLoginView.as_view(template_name='registration/login.html'), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]

urlpatterns += router.urls

# login (done)
# logout (done)
# signup (done)
# password-reset request
# password-reset change-password
# password-reset done
