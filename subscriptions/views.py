
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Subscription
from products.models import Product

@login_required
def subscribe(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        want_renewal = request.POST.get('renewal') == 'on'
        payment_method = request.POST.get('payment_method') or None
        # Set a default renewal date if user opts-in (30 days from today)
        from datetime import date, timedelta
        renewal_date = date.today() + timedelta(days=30) if want_renewal else None
        sub = Subscription.objects.create(
            user=request.user,
            product=product,
            active=True,
            renewal_date=renewal_date,
            payment_method=payment_method,
        )
        messages.success(request, 'Subscription successful!')
        return redirect('subscriptions:list')
    return render(request, 'subscriptions/subscribe.html', {
        'product': product,
    })

@login_required
def subscription_list(request):
    subs = Subscription.objects.filter(user=request.user)
    return render(request, 'subscriptions/subscription_list.html', {'subscriptions': subs})
