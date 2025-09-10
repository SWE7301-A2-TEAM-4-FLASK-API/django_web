from django.db import models

class Metric(models.Model):
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    value = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    # Add other fields as needed

    def __str__(self):
        return f"{self.product.name} - {self.value} @ {self.timestamp}"
