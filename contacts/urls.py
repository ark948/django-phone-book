from django.urls import path
from contacts.views import (
    ContactsList, 
    ContactDetail, 
    contacts_index, 
    new_contact_quick_process, 
    new_contact
    )

app_name = 'contacts'
urlpatterns = [
    path("api/<int:pk>/", ContactDetail.as_view(), name="contact-detail"),
    path("api/", ContactsList.as_view(), name="contacts-list"),
    path("new-contact-quick/", new_contact_quick_process, name="new-contact-quick"),
    path("new-contact/", new_contact, name="new-contact"),
    path("", contacts_index, name="index"),
]