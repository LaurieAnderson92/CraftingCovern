from django.shortcuts import render, reverse

from.forms import OrderForm
from products.models import Product

def checkout(request, id):

    product = Product.objects.filter(id=id).get()
    order_form = OrderForm()
    template = "checkout/checkout.html"
    context = {
        'order_form': order_form,
        'product': product,
        'stripe_public_key': 'pk_test_51QaJrSQOfy7uSMypuUYoHX35Eg0mQzBYTVpcxRzz4M6ZGCgumPWFSkKn2gbtNmDaHTFBiYUXztpKvSx5PK4eMK2J00ed1V6dMb',
        'client_secret': 'test client secret',
    }

    return render(request, template, context)