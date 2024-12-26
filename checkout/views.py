from django.shortcuts import render, reverse

from.forms import OrderForm
from products.models import Product

def checkout(request, id):

    product = Product.objects.filter(id=id).get()
    order_form = OrderForm()
    template = "checkout/checkout.html"
    context = {
        'order_form': order_form,
        'product': product
    }

    return render(request, template, context)