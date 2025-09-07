
from django.conf import settings
from django.db import models
from products.models import Product

class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    started_at = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=True)
    renewal_date = models.DateField(null=True, blank=True)
    payment_method = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} → {self.product.name}'
