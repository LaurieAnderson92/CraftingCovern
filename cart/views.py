from django.shortcuts import render

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

