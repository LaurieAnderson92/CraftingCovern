from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.conf import settings
from django.contrib import messages

from.forms import OrderForm
from products.models import Product
from .models import Order

import stripe

def checkout(request, id):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    query = Profile.objects.all()
    profile_id = request.user.pk
    profile = get_object_or_404(query, auth_user_id=profile_id)

    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        messages.error(request, f'The product could not be found, please contact an administrator ')

    product_cost = product.cost
    tenpercernt = product_cost/10
    delivery_cost = 0

    if tenpercernt > settings.MINIMUM_DELIVERY_CHARGE:
        delivery_cost = tenpercernt
    else:
        delivery_cost = settings.MINIMUM_DELIVERY_CHARGE

    grand_total = product_cost + delivery_cost
    stripe_total = round(grand_total * 100)

    if request.method == 'POST':
        product = Product.objects.get(id=id)
        customer = request.user
        form_data = {
            'customer': customer,
            'product': product,
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST.get('street_address2'),
            'county': request.POST.get('county'),
            'delivery_cost': delivery_cost,
            'order_cost': product_cost,
            'grand_total': grand_total,
        }
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save()
            return redirect(reverse('checkout_success', args=[order.order_number]))
        else:
            messages.error(request, f'An Error has occurred, your card has not been charged.')
    else:
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
            'delivery_cost': delivery_cost,
            'grand_total': grand_total,
            'profile': profile
        }
    return render(request, template, context)

def checkout_success(request, order_number):
    """
    This View handles successful checkouts
    """
    query = Profile.objects.all()
    profile_id = request.user.pk
    profile = get_object_or_404(query, auth_user_id=profile_id)

    order = get_object_or_404(Order, order_number=order_number)
    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'profile': profile,
    }
    messages.success(request, f'Your order of ' + order.product.name + ' has been placed.')
    return render(request, template, context)