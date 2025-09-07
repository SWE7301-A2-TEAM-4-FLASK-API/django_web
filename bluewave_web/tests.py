from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.conf import settings
from django.middleware.csrf import CsrfViewMiddleware
from django.contrib.auth.hashers import identify_hasher
from django.db import connection
from django.http import HttpResponse
from django.template import Context, Template


@override_settings(DATABASES={
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
})
class SecurityTests(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)

    def test_csrf_protection_rejects_missing_token(self):
        # POST to a known POSTing endpoint: accounts:login
        url = reverse('accounts:login')
        resp = self.client.post(url, data={'username': 'x', 'password': 'y', 'role': 'user'})
        self.assertEqual(resp.status_code, 403)

    def test_security_headers_present(self):
        resp = self.client.get('/')
        # SecurityMiddleware/XFrameOptions
        self.assertIn('X-Content-Type-Options', resp.headers)
        self.assertEqual(resp.headers.get('X-Content-Type-Options'), 'nosniff')
        self.assertIn('X-Frame-Options', resp.headers)
        self.assertEqual(resp.headers.get('X-Frame-Options'), 'DENY')
        self.assertIn('Referrer-Policy', resp.headers)

    def test_passwords_hashed(self):
        User = get_user_model()
        u = User.objects.create_user(username='alice', password='SuperStrong!123')
        # Raw password should not equal stored value; hasher should be identifiable
        self.assertNotEqual(u.password, 'SuperStrong!123')
        hasher = identify_hasher(u.password)
        self.assertTrue(hasher)

    def test_templates_autoescape_by_default(self):
        # Render a template without autoescape off; HTML should be escaped
        tmpl = Template('{{ payload }}')
        rendered = tmpl.render(Context({'payload': '<script>alert(1)</script>'}))
        self.assertNotIn('<script>', rendered)
        self.assertIn('&lt;script&gt;', rendered)

    def test_session_cookie_flags(self):
        # Verify configuration of session and CSRF cookie flags
        self.assertTrue(settings.SESSION_COOKIE_HTTPONLY)
        self.assertTrue(settings.CSRF_COOKIE_HTTPONLY)
        self.assertIn(settings.SESSION_COOKIE_SAMESITE, ('Lax', 'Strict', 'None'))
        self.assertIn(settings.CSRF_COOKIE_SAMESITE, ('Lax', 'Strict', 'None'))
    # Note: in tests, Django may set DEBUG=False but not recompute cookie flags.
    # Production enforcement of SECURE flags is documented and environment-driven.

    def test_orm_prevents_sql_injection_in_filter(self):
        # Attempt an injection in a harmless query; ORM should escape it, not error or run extra commands
        from products.models import Product
        Product.objects.create(name='A', description='d', price=1, stock=1)
        malicious = "1'; DROP TABLE products_product; --"
        qs = list(Product.objects.filter(name=malicious))
        # Table should still exist and query should succeed harmlessly
        with connection.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM products_product")
            count = cur.fetchone()[0]
        self.assertGreaterEqual(count, 1)