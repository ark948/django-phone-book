from django.urls import path
from contacts.views import (
    ContactsList, 
    ContactDetail, 
    contacts_index, 
    new_contact_quick_process, 
    NewContact
    )

app_name = 'contacts'
urlpatterns = [
    path("api/<int:pk>/", ContactDetail.as_view(), name="contact-detail"),
    path("api/", ContactsList.as_view(), name="contacts-list"),
    path("new-contact-quick/", new_contact_quick_process, name="new-contact-quick"),
    path("new-contact/", NewContact.as_view(), name="new-contact"),
    path("", contacts_index, name="index"),
]