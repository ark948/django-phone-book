from django.urls import path
from contacts.views import ContactsList, ContactDetail

app_name = 'contacts'
urlpatterns = [
    path("<int:pk>/", ContactDetail.as_view(), name="contact-detail"),
    path("", ContactsList.as_view(), name="contacts-list"),
]