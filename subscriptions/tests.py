from django.test import TestCase

# Create your tests here.

# subscriptions/tests.py
from django.test import TestCase, Client

class SubscriptionTests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_subscription_creation(self):
        response = self.client.post('/subscriptions/subscribe/', {
            'product_id': 1,
            'user_id': 1
        })
        self.assertEqual(response.status_code, 201)

    def test_subscription_list(self):
        response = self.client.get('/subscriptions/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Subscriptions")
        self.assertIsInstance(response.json(), list)