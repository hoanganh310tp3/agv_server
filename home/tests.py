from django.test import TestCase
from django.test import SimpleTestCase
# Create your tests here.
class SimpleTestCase(SimpleTestCase):
    def test_home_page_status(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code,200)