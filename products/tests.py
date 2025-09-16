from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from .models import Product


class ProductViewsTests(TestCase):
	def setUp(self):
		self.client = Client()
		self.product = Product.objects.create(name='P1', description='D', price='9.99', stock=5)
		User = get_user_model()
		self.user = User.objects.create_user(username='bob', email='b@example.com', password='pass1234')

	def test_product_list(self):
		resp = self.client.get('/products/')
		self.assertEqual(resp.status_code, 200)
		self.assertContains(resp, 'P1')

	def test_product_detail(self):
		resp = self.client.get(f'/products/{self.product.id}/')
		self.assertEqual(resp.status_code, 200)
		self.assertContains(resp, 'P1')

	def test_subscribe_redirects_to_subscriptions(self):
		# Must be logged in
		self.client.login(username='bob', password='pass1234')
		resp = self.client.get(f'/products/{self.product.id}/subscribe/')
		self.assertEqual(resp.status_code, 302)
		self.assertIn('/subscriptions/subscribe/', resp['Location'])
