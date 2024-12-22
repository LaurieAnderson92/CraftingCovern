from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from .models import User

# Create your views here.

def user_detail(request, id):
    query = User.objects.all()
    print("this is query = ",query)

    user = get_object_or_404(query, id=id)
    print("this is user = ",user)

    return render(
        request,
        'users/user_detail.html',
        {'user': user }
    )

