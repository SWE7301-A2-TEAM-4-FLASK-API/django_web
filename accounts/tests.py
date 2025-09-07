 
# accounts/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
 

class AccountTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.User = get_user_model()

    def test_user_registration(self):
        response = self.client.post(reverse('accounts:register'), {
            'username': 'testuser',
            'password1': 'StrongPass!123',
            'password2': 'StrongPass!123',
            'role': 'consumer'
        })
        self.assertEqual(response.status_code, 302)  # Redirect on success
        user_exists = self.User.objects.filter(username='testuser').exists()
        self.assertTrue(user_exists)

    def test_user_login(self):
        self.User.objects.create_user(username='testuser', password='StrongPass!123', role='consumer')
        response = self.client.post(reverse('accounts:login'), {
            'username': 'testuser',
            'password': 'StrongPass!123',
            'role': 'consumer'
        })
        self.assertEqual(response.status_code, 302)  # Redirect on success
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_user_profile_access(self):
        user = self.User.objects.create_user(username='testuser', password='StrongPass!123', role='consumer')
        self.client.login(username='testuser', password='StrongPass!123')
        response = self.client.get(reverse('accounts:user'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser')