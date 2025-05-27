# views.py
from django.shortcuts import render, redirect, get_object_or_404
from services.models import Service
import stripe
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


stripe.api_key = settings.STRIPE_SECRET_KEY


def cart_view(request):
    cart = request.session.get('cart', {})
    service_ids = list(cart.keys())

    services = Service.objects.filter(id__in=service_ids)

    cart_items = []
    total_price = 0

    for service in services:
        total_price += service.price
        cart_items.append({
            'service': service,
            'total': service.price,
        })

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'cart/cart.html', context)


def add_to_cart(request, service_id):
    cart = request.session.get('cart', {})
    cart[str(service_id)] = 1  # Set to 1 (default) since no quantity is needed
    request.session['cart'] = cart
    return redirect('cart')


def remove_from_cart(request, service_id):
    cart = request.session.get('cart', {})
    service_id_str = str(service_id)
    if service_id_str in cart:
        del cart[service_id_str]
        request.session['cart'] = cart
    return redirect('cart')


def update_cart_quantity(request, service_id):
    if request.method == "POST":
        quantity = int(request.POST.get('quantity', 1))
        cart = request.session.get('cart', {})
        if quantity > 0:
            cart[str(service_id)] = quantity
        else:
            cart.pop(str(service_id), None)
        request.session['cart'] = cart
    return redirect('cart')


def success_view(request):
    return render(request, 'cart/success.html')


def cancel_view(request):
    return render(request, 'cart/cancel.html')


@login_required
def create_checkout_session(request):
    cart = request.session.get('cart', {})
    services = Service.objects.filter(id__in=cart.keys())

    line_items = []
    for service in services:
        line_items.append({
            'price_data': {
                'currency': 'eur',
                'product_data': {
                    'name': service.title,
                },
                'unit_amount': int(service.price * 100),  # Stripe uses cents
            },
            'quantity': 1,
        })

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=request.build_absolute_uri('/cart/success/'),
        cancel_url=request.build_absolute_uri('/cart/cancel/'),
    )
    return redirect(session.url)