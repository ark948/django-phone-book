from django.test import TestCase
from contacts.models import Contact
from django.contrib.auth import get_user_model

class ContactModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        get_user_model().objects.create(username="testuser", password='hello123*')
        Contact.objects.create(title="friend", owner=get_user_model().objects.get(id=1))
        cls.contact = Contact.objects.get(id=1)

    def test_all_field_labels(self):
        title_label = self.contact._meta.get_field('title').verbose_name
        first_name_label = self.contact._meta.get_field('first_name').verbose_name
        last_name_label = self.contact._meta.get_field('last_name').verbose_name
        phone_number_label = self.contact._meta.get_field('phone_number').verbose_name
        email_field_label = self.contact._meta.get_field('email').verbose_name
        address_field_label = self.contact._meta.get_field('address').verbose_name
        date_created_label = self.contact._meta.get_field('date_created').verbose_name
        last_modified_label = self.contact._meta.get_field('last_modified').verbose_name
        self.assertEqual(title_label, "Title")
        self.assertEqual(first_name_label, 'First Name')
        self.assertEqual(last_name_label, "Last Name")
        self.assertEqual(phone_number_label, "Phone/Cell Number")
        self.assertEqual(email_field_label, "Email Address")
        self.assertEqual(address_field_label, "Address")
        self.assertEqual(date_created_label, "Created on")
        self.assertEqual(last_modified_label, "Modified on")

    def test_title_max_length(self):
        max_length = self.contact._meta.get_field('title').max_length
        self.assertEqual(max_length, 200)

    def test_user_owns_contact(self):
        owner = self.contact.owner
        self.assertTrue(isinstance(owner, get_user_model()))

    def test_get_absolute_url(self):
        self.assertEqual(self.contact.get_absolute_url(), '/contacts/api/1/')

# all labels (done)
# lengths
# absolute url (done)
# moving contact instance to setuptestdata