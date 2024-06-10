from contacts.forms import NewContactForm, NewContactQuickForm
from django.test import TestCase, SimpleTestCase

class NewContactFormTest(SimpleTestCase):
    # @classmethod
    # def setUpTestData(cls) -> None:
    #     cls.form = NewContactForm()

    def setUp(self) -> None:
        self.form = NewContactForm()
        return super().setUp()

    def test_field_labels(self):
        self.assertEqual(self.form.fields["title"].label, "عنوان:")
        self.assertEqual(self.form.fields["first_name"].label, "نام:")
        self.assertEqual(self.form.fields["last_name"].label, "نام خانوادگی:")
        self.assertEqual(self.form.fields["phone_number"].label, "شماره تماس:")
        self.assertEqual(self.form.fields["email"].label, "ایمیل:")
        self.assertEqual(self.form.fields["address"].label, "آدرس:")

# labels (done)
# lengths
# help texts
# extra or any custom validation