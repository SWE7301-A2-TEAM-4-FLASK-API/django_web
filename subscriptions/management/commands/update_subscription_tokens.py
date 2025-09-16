from django.core.management.base import BaseCommand
from subscriptions.models import Subscription
from django.conf import settings
import jwt
import datetime

class Command(BaseCommand):
    help = 'Update all subscriptions with a JWT api_token if missing.'

    def handle(self, *args, **options):
        updated = 0
        for sub in Subscription.objects.filter(api_token__isnull=True):
            payload = {
                'sub_id': sub.id,
                'user_id': sub.user_id,
                'product_id': sub.product_id,
                'plan': sub.plan,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30)
            }
            secret = getattr(settings, 'JWT_SECRET')
            sub.api_token = jwt.encode(payload, secret, algorithm='HS256')
            sub.save()
            updated += 1
        self.stdout.write(self.style.SUCCESS(f'Updated {updated} subscriptions with JWT tokens.'))
