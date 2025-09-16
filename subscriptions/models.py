from django.db import models
from django.conf import settings
from products.models import Product

class Subscription(models.Model):
    PLAN_CHOICES = [
        ('day', 'Day'),
        ('week', 'Week'),
        ('month', 'Month'),
        ('year', 'Year'),
    ]
    PAYMENT_METHODS = [
        ('card', 'Card'),
        ('paypal', 'PayPal'),
        ('bank', 'Bank Transfer'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    plan = models.CharField(max_length=10, choices=PLAN_CHOICES)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    auto_renewal = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    status = models.CharField(max_length=20, default='active')
    api_token = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.api_token:
            import jwt
            from django.conf import settings
            import datetime
            payload = {
                'sub_id': self.id if self.id else None,
                'user_id': self.user_id,
                'product_id': self.product_id,
                'plan': self.plan,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30)
            }
            secret = getattr(settings, 'JWT_SECRET', 'your_jwt_secret_key')
            self.api_token = jwt.encode(payload, secret, algorithm='HS256')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} - {self.product} ({self.plan})"
