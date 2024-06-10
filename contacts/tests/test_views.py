from django.test import TestCase
from contacts.models import Contact
from django.urls import reverse
from django.contrib.auth import get_user_model
from icecream import ic
from accounts.models import CustomUser

# User = get_user_model()


class ContactsViewsTest(TestCase):
    def setUp(self) -> None:
        self.test_user = CustomUser.objects.create()
        self.test_user.username = "testuser1"
        self.test_user.set_password("hello123*ABC")
        self.test_user.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("contacts:index"))
        self.assertRedirects(response, "/accounts/login/?next=/contacts/")

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username="testuser1", password="hello123*ABC")
        response = self.client.get(reverse("contacts:index"))
        ic(login)     

        # check if user logged in
        self.assertEqual(str(response.context["user"]), 'testuser1')

        # check if response was success
        self.assertEqual(response.status_code, 200)

        # check if template was correct
        self.assertTemplateUsed(response, "contacts/index.html")

    def test_contact_detail_page_is_accessible(self):
        login = self.client.login(username="testuser1", password="hello123*ABC")
        Contact.objects.create(title="test", owner=CustomUser.objects.get(id=1))
        self.contact_item = Contact.objects.get(id=1)
        owner = self.contact_item.owner
        self.assertTrue(isinstance(owner, get_user_model()))
        response = self.client.get(reverse("contacts:contact-detail", kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)


# urls (both with reverse and manual)
# template used
# pagination
# test second page (as an example)