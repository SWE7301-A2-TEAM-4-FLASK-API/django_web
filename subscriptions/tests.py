from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from products.models import Product
from subscriptions.models import Subscription


class SubscriptionTests(TestCase):

    def setUp(self):
        self.client = Client()
        User = get_user_model()
        self.user = User.objects.create_user(username='alice', email='a@example.com', password='pass1234')
        self.product = Product.objects.create(name='Test Product', description='desc', price='9.99', stock=10)
        # login the user
        self.client.login(username='alice', password='pass1234')

    def test_subscription_creation(self):
        url = f'/subscriptions/subscribe/{self.product.id}/'
        resp = self.client.post(url, {
            'product': self.product.id,
            'plan': 'month',
            'payment_method': 'card',
            'auto_renewal': True,
        })
        # Expect redirect to list on success
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp['Location'], '/subscriptions/')
        self.assertTrue(Subscription.objects.filter(user=self.user, product=self.product, plan='month').exists())

    def test_subscription_list(self):
        # Ensure the page loads for an authenticated user
        resp = self.client.get('/subscriptions/')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'My Subscriptions')