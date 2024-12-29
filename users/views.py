from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from django.contrib import messages

from .models import Profile, Newsletter
from .forms import NewsletterSignupForm
from checkout.models import Order

# Create your views here.

@login_required
def profile_detail(request, id):
    query = Profile.objects.all()
    profile = get_object_or_404(query, auth_user_id=id)
    profile_id = profile.auth_user_id
    orders = Order.objects.filter(customer=profile_id).order_by('-date')
    already_regsistered = False
    already_regsistered_id = 0
    newsletter_recipients = Newsletter.objects.all().order_by('-subscribed_on')

    for recipient in newsletter_recipients:
        if recipient.profile.pk == profile.auth_user.pk:
            already_regsistered_id = recipient.pk
            already_regsistered = True

    if request.method == 'POST':
        form_data = {
            'email': request.POST['email'],
            'profile': profile_id
        }
        form = NewsletterSignupForm(form_data)
        if form.is_valid():
            if already_regsistered:
                form.save()
                messages.sucess(request, "Email updated successfully.")
            else:
                form = NewsletterSignupForm(form_data, instance=newsletter_recipients.get(pk=already_regsistered_id))
                form.save()
                messages.success(request, "Thank you for subscribing!")
    else:
        form = NewsletterSignupForm()
    
    context = {
        'profile': profile,
        'orders': orders,
        'form': form,
        'recipients': newsletter_recipients,
        'already_regsistered': already_regsistered,
        'already_regsistered_id': already_regsistered_id
    }
    
    return render(
        request,
        'users/profile_detail.html',
        context
    )

def newsletter_delete(request, pk):
    profile = request.user.pk
    recipient = get_object_or_404(Newsletter, pk=pk)
    recipient.delete()
    messages.success(request, "Successfully unsubscribed.")
    return redirect ('profile_detail', profile)
