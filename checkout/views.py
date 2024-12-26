from django.shortcuts import render, reverse
from django.conf import settings

from.forms import OrderForm
from products.models import Product

import stripe

def checkout(request, id):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    product = Product.objects.filter(id=id).get()
    product_cost = product.cost
    tenpercernt = product_cost/10
    delivery_cost = 0

    if tenpercernt > settings.MINIMUM_DELIVERY_CHARGE:
        delivery_cost = tenpercernt
    else:
        delivery_cost = settings.MINIMUM_DELIVERY_CHARGE

    stripe_total = round((product_cost + delivery_cost) * 100)

    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

    order_form = OrderForm()
    template = "checkout/checkout.html"
    context = {
        'order_form': order_form,
        'product': product,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)