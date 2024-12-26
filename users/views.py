from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from .models import Profile

# Create your views here.

@login_required
def profile_detail(request, id):
    query = Profile.objects.all()
    profile = get_object_or_404(query, auth_user_id=id)

    return render(
        request,
        'users/profile_detail.html',
        {'profile': profile }
    )

