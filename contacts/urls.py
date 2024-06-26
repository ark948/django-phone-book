from django.urls import path
from contacts.views import (
    ContactsList, 
    ContactDetail, 
    contacts_index, 
    new_contact_quick_process, 
    new_contact,
    delete_contact,
    edit_contact,
    edit_contact_process,
    download_csv
    )

app_name = 'contacts'
urlpatterns = [
    path("api/<int:pk>/", ContactDetail.as_view(), name="contact-detail"),
    path("api/", ContactsList.as_view(), name="contacts-list"),
    path("new-contact-quick/", new_contact_quick_process, name="new-contact-quick"),
    path("new-contact/", new_contact, name="new-contact"),
    path("delete-contact/", delete_contact, name="delete-contact"),
    path("edit-contact/", edit_contact, name="edit-contact"),
    path("edit-contact-process/", edit_contact_process, name="edit-contact-process"),
    path("download-csv/", download_csv, name="download-csv"),
    path("", contacts_index, name="index"),
]