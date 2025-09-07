from django.core.management.base import BaseCommand
from products.models import Product


SAMPLES = [
    {
        "name": "BlueWave Nano-10",
        "description": "Compact micro-desalination unit for small households and field kits.",
        "price": 399.99,
        "stock": 25,
    },
    {
        "name": "BlueWave Nano-20",
        "description": "Portable unit with double-stage filtration for improved taste.",
        "price": 549.00,
        "stock": 18,
    },
    {
        "name": "BlueWave Solo",
        "description": "Single-user hand-pump desalination ideal for emergencies.",
        "price": 199.00,
        "stock": 60,
    },
    {
        "name": "BlueWave Duo",
        "description": "Two-user manual desalination with carbon post-filter.",
        "price": 279.00,
        "stock": 40,
    },
    {
        "name": "BlueWave Go",
        "description": "Battery-powered portable unit for campers and researchers.",
        "price": 699.00,
        "stock": 15,
    },
    {
        "name": "BlueWave Pro-50",
        "description": "Professional-grade system with smart monitoring integration.",
        "price": 1499.00,
        "stock": 10,
    },
    {
        "name": "BlueWave Pro-100",
        "description": "High-capacity desalination for small communities or ships.",
        "price": 2899.00,
        "stock": 6,
    },
    {
        "name": "BlueWave Solar Mini",
        "description": "Solar-assisted unit optimizing output with real-time metrics.",
        "price": 899.00,
        "stock": 20,
    },
    {
        "name": "BlueWave Solar Pro",
        "description": "Off-grid solar desalination bundle with storage tank.",
        "price": 3299.00,
        "stock": 5,
    },
    {
        "name": "BlueWave Lab Kit",
        "description": "Educational desalination kit for classrooms and workshops.",
        "price": 149.00,
        "stock": 80,
    },
    {
        "name": "BlueWave Lab Pro",
        "description": "Advanced educational kit with real-time monitoring.",
        "price": 249.00,
        "stock": 30,
    },
]


class Command(BaseCommand):
    help = "Seed 10 sample products into the database"

    def handle(self, *args, **options):
        created = 0
        for item in SAMPLES:
            obj, was_created = Product.objects.get_or_create(
                name=item["name"],
                defaults={
                    "description": item["description"],
                    "price": item["price"],
                    "stock": item["stock"],
                },
            )
            created += 1 if was_created else 0

        self.stdout.write(self.style.SUCCESS(f"Seed complete. {created} new products added."))
