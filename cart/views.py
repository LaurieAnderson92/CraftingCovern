from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from users.models import Profile

# Create your views here.

def cart_list(request):
    """A view to Return the cart list Page"""
    try:
        profile_query = Profile.objects.all()
        profile_id = request.user.pk
        profile = get_object_or_404(profile_query, auth_user_id=profile_id)
        context = {
            'profile': profile,
        }
        return render(request, 'cart/cart.html', context)
    except Exception as e:
        return render(request, 'cart/cart.html')


def add_to_cart(request, item_id,):
    """ Add a quantity of the specified product to the shopping cart """

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    cart = request.session.get('cart', {})
    if item_id in list(cart.keys()):
        cart[item_id] += quantity
    else:
        cart[item_id] = quantity

    request.session['cart'] = cart
    return redirect(redirect_url)

def update_cart(request, item_id,):
    """ Update the quantity of a specified product to the shopping cart """

    quantity = int(request.POST.get('quantity'))
    cart = request.session.get('cart', {})
    if quantity > 0:
        cart[item_id] = quantity
    else:
        cart.pop[item_id]

    request.session['cart'] = cart
    return redirect(reverse('cart'))

def remove_cart(request, item_id,):
    """ Update the quantity of a specified product to the shopping cart """
    cart = request.session.get('cart', {})
    cart.pop(item_id)
    request.session['cart'] = cart
    return HttpResponse(status=200)
    