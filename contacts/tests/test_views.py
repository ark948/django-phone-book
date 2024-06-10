from django.test import TestCase
from contacts.models import Contact
from django.urls import reverse
from django.contrib.auth import get_user_model
from icecream import ic
from accounts.models import CustomUser

# User = get_user_model()


class ContactsViewsTest(TestCase):
    def setUp(self) -> None:
        test_user = CustomUser.objects.create()
        test_user.username = "testuser1"
        test_user.set_password("hello123*ABC")
        test_user.save()

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

# urls (both with reverse and manual)
# template used
# pagination
# test second page (as an example)