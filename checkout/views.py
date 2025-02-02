from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.conf import settings
from django.contrib import messages
from users.models import Profile
import stripe
from decimal import Decimal
from django.core.mail import send_mail


from products.models import Product
from .forms import OrderForm
from .models import Order, OrderLineItem
from cart.contexts import cart_contents

def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "There is nothing in your cart at the moment")
        return redirect(reverse('product_all'))

    order_form = OrderForm()
    current_cart = cart_contents(request)

    order_cost = current_cart['total']
    delivery_cost = current_cart['delivery_cost']
    grand_total = current_cart['grand_total']

    stripe_total = round(grand_total * 100)
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
        )

    if request.method == 'POST':
        if request.user.is_authenticated:
            customer = request.user
        else:
            customer = None
        from_email = settings.EMAIL_HOST_USER
        to_email = request.POST['email']
        form_data = {
            'customer': customer,
            'full_name': request.POST['full_name'],
            'email': to_email,
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
            'customization': request.POST['customization'],
            'delivery_cost': delivery_cost,
            'order_cost': order_cost,
            'grand_total': grand_total,
        }
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save()
            for item_id, total_quantity in cart.items():
                product = Product.objects.get(id=item_id)
                for i in range(total_quantity):
                    try:
                        OrderLineItem.objects.create(
                            order=order,
                            product=product,
                            lineitem_cost=product.cost
                        )
                    except Product.DoesNotExist:
                        messages.error(request, (
                            """Error, the order could not be created,
                            please contact us for assistance""")
                        )
                        order.delete()
                        return redirect(reverse('view_cart'))
            try:
                subject = f'Your Coven Crafts Order:{order.order_number}'
                body = f'''Thank you for your order with Coven crafts!
                    Your order Total is: {grand_total}
                    Your order will be Shipped as soon as it has been crafted!'''
                send_mail(
                    subject,
                    body,
                    from_email,
                    [to_email]
                )
                del request.session['cart']
                return redirect(reverse('checkout_success', args=[order.order_number])
            )
            except Exception as e:
                print(e) 
                messages.error(request, ("There was an Error generating your Email, please contact us"))
                reverse('checkout_success', args=[order.order_number])
        else:
            messages.error(
                request,
                f'An Error has occurred, your card has not been charged.'
                )
    else:
        try:
            profile_query = Profile.objects.all()
            profile_id = request.user.pk
            profile = get_object_or_404(profile_query, auth_user_id=profile_id)
            context = {
                'order_form': order_form,
                'stripe_public_key': stripe_public_key,
                'client_secret': intent.client_secret,
                'delivery_cost': delivery_cost,
                'grand_total': grand_total,
                'profile': profile,
            }
        except Exception as e:
            context = {
                'order_form': order_form,
                'stripe_public_key': stripe_public_key,
                'client_secret': intent.client_secret,
                'delivery_cost': delivery_cost,
                'grand_total': grand_total,
            }        
    template = "checkout/checkout.html"
    return render(request, template, context)


def checkout_success(request, order_number):
    """
    This View handles successful checkouts
    """
    query = Profile.objects.all()
    profile_id = request.user.pk
    order = get_object_or_404(Order, order_number=order_number)
    template = 'checkout/checkout_success.html'

    try:
        profile = get_object_or_404(query, auth_user_id=profile_id)
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
        f'Your order: {order_number} has been placed.')
    return render(request, template, context)
