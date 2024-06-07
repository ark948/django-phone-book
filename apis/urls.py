from django.urls import path, include
from apis.views import index

app_name="apis"
urlpatterns = [
    path("", index, name="index"),
    path("contacts/", include("contacts.urls")),
    path("accounts/", include("accounts.urls")),
]