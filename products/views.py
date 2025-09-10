from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product

def product_list(request):
    products = Product.objects.all()[:6]  # Show a few products on homepage
    return render(request, 'products/product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})

@login_required
def subscribe_product(request, pk):
    # Redirect to subscription page for this product
    return redirect('subscriptions:subscribe', product_id=pk)
