from django.test import TestCase
from django.contrib.auth import get_user_model
from contacts.models import Contact

# Create your tests here.

class ContactsTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = get_user_model().objects.create_user(username='testuser', email='test@email.com', password='secret')
        cls.contact = Contact.objects.create(owner=cls.user, title='friend')
        return super().setUpTestData()
    
    def test_contact_model(self):
        self.assertTrue(isinstance(self.contact, Contact))
        self.assertEqual(self.contact.title, 'friend')
        self.assertEqual(self.contact.owner.username, 'testuser')
        self.assertEqual(self.contact.owner, self.user)

    def test_contact_api(self):
        # this is just to check if test module works fine
        self.assertEqual(1, 1)
