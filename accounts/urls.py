from django.urls import path
from accounts.views import UserList, UserDetail, UserViewSet
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(r"users", UserViewSet)

urlpatterns = router.urls