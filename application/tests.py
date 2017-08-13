from django.test import TestCase
from django.test.client import RequestFactory

from .views import index

# Create your tests here.
class OtherTest(TestCase):

    def test_basic(self):
        factory = RequestFactory()
        request = factory.get('/')

        response = index(request)
        self.assertEqual(200, response.status_code)