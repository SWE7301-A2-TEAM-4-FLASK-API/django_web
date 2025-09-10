from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import SubscriptionForm
from .models import Subscription
from products.models import Product
from metrics.services import get_jwt_token
from datetime import datetime, timedelta

@login_required
def subscribe(request, product_id):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            subscription = form.save(commit=False)
            subscription.user = request.user
            subscription.start_date = datetime.now()
            product = Product.objects.get(id=product_id)
            subscription.product = product
            subscription.price = product.price
            plan = subscription.plan
            duration = {'day': 1, 'week': 7, 'month': 30, 'year': 365}[plan]
            subscription.end_date = subscription.start_date + timedelta(days=duration)
            if subscription.payment_method:
                subscription.status = 'active'
            # Generate token for this subscription
            subscription.api_token = get_jwt_token(request.user.username, None, request.user.role)
            subscription.save()
            return redirect('subscriptions:list')
    else:
        form = SubscriptionForm()
    return render(request, 'subscriptions/subscribe.html', {'form': form})

@login_required
def subscription_list(request):
    subs = Subscription.objects.filter(user=request.user)
    return render(request, 'subscriptions/subscription_list.html', {'subscriptions': subs})

@login_required
def toggle_renewal(request, sub_id):
    sub = Subscription.objects.get(id=sub_id, user=request.user)
    sub.auto_renewal = not sub.auto_renewal
    sub.save()
    return redirect('subscriptions:list')

@login_required
def cancel_subscription(request, sub_id):
    sub = Subscription.objects.get(id=sub_id, user=request.user)
    sub.status = 'cancelled'
    sub.auto_renewal = False
    sub.save()
    return redirect('subscriptions:list')
