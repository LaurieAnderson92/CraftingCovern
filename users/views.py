from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from .models import Profile

# Create your views here.

def profile_detail(request, id):
    query = Profile.objects.all()
    #print("this is query = ",query)

    profile = get_object_or_404(query, id=id)
    #print("this is user = ",user)

    return render(
        request,
        'users/profile_detail.html',
        {'user': profile }
    )

