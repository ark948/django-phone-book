from django.test import TestCase
from django.urls import reverse

# Create your tests here.

class PagesViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:

        return super().setUpTestData()
    
    def test_pages_index_exists_at_correct_location(self):
        response = self.client.get("")
        self.assertEqual(response.status_code, 200)

    def test_pages_index_url_by_endpoint(self):
        response = self.client.get(reverse("pages:index"))
        self.assertEqual(response.status_code, 200)

    def test_pages_index_template(self):
        response = self.client.get(reverse("pages:index"))
        self.assertTemplateUsed(response, "pages/index.html")