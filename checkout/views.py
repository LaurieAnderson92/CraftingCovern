from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.conf import settings
from django.contrib import messages
from products.models import Product
from users.models import Profile
import stripe
from decimal import Decimal

from .forms import OrderForm
from .models import Order
from cart.contexts import cart_contents

def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "There is nothing in your cart at the moment")
        return redirect(reverse('products_all'))

    total = 0

    for item_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=item_id)
        total += quantity * product.cost
    tenpercernt = total/10
    delivery_cost = 0

    if tenpercernt > settings.MINIMUM_DELIVERY_CHARGE:
        delivery_cost = Decimal(tenpercernt)
    else:
        delivery_cost = settings.MINIMUM_DELIVERY_CHARGE

    grand_total = total + delivery_cost

    order_form = OrderForm()
    template = "checkout/checkout.html"
    context = {
        'order_form': order_form,
        'delivery_cost': delivery_cost,
    }

    return render(request, template, context)

# DEPRICATED
# def checkout(request):
#     cart = request.session.get('cart', {})
#     if not cart:
#         messages.error(request, "There is nothing in your cart at the moment")
#         return redirect(reverse('products_all'))

#     stripe_public_key = settings.STRIPE_PUBLIC_KEY
#     stripe_secret_key = settings.STRIPE_SECRET_KEY

#     query = Profile.objects.all()
#     profile_id = request.user.pk
#     delivery_cost = cart_contents.delivery_cost
#     grand_total = cart_contents.grand_total

#     order_form = OrderForm()
#     template = "checkout/checkout.html"
#     context = {}
#     # stripe_total = round(grand_total * 100)
#     stripe.api_key = stripe_secret_key
#     # intent = stripe.PaymentIntent.create(
#     #     amount=stripe_total,
#     #     currency=settings.STRIPE_CURRENCY,
#     #     )
    

#     if request.method == 'POST':
#         product = Product.objects.get(id=id)
#         customer = request.user
#         form_data = {
#             'customer': customer,
#             'full_name': request.POST['full_name'],
#             'email': request.POST['email'],
#             'phone_number': request.POST['phone_number'],
#             'country': request.POST['country'],
#             'postcode': request.POST['postcode'],
#             'town_or_city': request.POST['town_or_city'],
#             'street_address1': request.POST['street_address1'],
#             'street_address2': request.POST.get('street_address2'),
#             'county': request.POST.get('county'),
#             'delivery_cost': delivery_cost,
#             'order_cost': product_cost,
#             'grand_total': grand_total,
#         }
#         order_form = OrderForm(form_data)
#         if order_form.is_valid():
#             order = order_form.save()
#             return redirect(
#                 reverse('checkout_success', args=[order.order_number])
#                 )
#         else:
#             messages.error(
#                 request,
#                 f'An Error has occurred, your card has not been charged.'
#                 )
#     else:
#         try:
#             profile = get_object_or_404(query, auth_user_id=profile_id)
#             context = {
#                 'order_form': order_form,
#                 'stripe_public_key': stripe_public_key,
#                 # 'client_secret': intent.client_secret,
#                 'delivery_cost': delivery_cost,
#                 'grand_total': grand_total,
#                 'profile': profile
#             }
#         except Exception as e:
#             context = {
#                 'order_form': order_form,
#                 'stripe_public_key': stripe_public_key,
#                 # 'client_secret': intent.client_secret,
#                 'delivery_cost': delivery_cost,
#                 'grand_total': grand_total,
#             }
#     return render(request, template, context)


def checkout_success(request, order_number):
    """
    This View handles successful checkouts
    """
    query = Profile.objects.all()
    profile_id = request.user.pk
    order = get_object_or_404(Order, order_number=order_number)
    template = 'checkout/checkout_success.html'
    context = {
            'order': order,
        }

    try:
        profile = get_object_or_404(query, auth_user_id=profile_id)
        print("Profile below:")
        print(profile)
        context = {
            'order': order,
            'profile': profile,
        }
    except Exception as e:
        context = {
            'order': order,
        }
    messages.success(
        request,
        f'Your order of ' + order.product.name + ' has been placed.')
    return render(request, template, context)
