from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect, reverse
from django.contrib import messages
from checkout.models import Order

from .models import Profile, Newsletter
from .forms import NewsletterSignupForm


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
        if already_regsistered:
            form = NewsletterSignupForm(
                form_data,
                instance=newsletter_recipients.get(
                    pk=already_regsistered_id
                )
            )
            form.save()
            messages.success(request, "Email updated successfully.")
            return HttpResponseRedirect(request.path_info)
        elif form.is_valid():
            form.save()
            messages.success(request, "Thank you for subscribing!")
            return HttpResponseRedirect(request.path_info)
        else:
            messages.error(
                request,
                "Something went wrong, please contact us if the issue persists"
            )
    else:
        if profile_id == request.user.id:
            form = NewsletterSignupForm()
            context = {
                'profile': profile,
                'orders': orders,
                'form': form,
                'already_regsistered': already_regsistered,
                'already_regsistered_id': already_regsistered_id
            }
            return render(
                request,
                'users/profile_detail.html',
                context
            )
        else:
            messages.warning(
                request,
                f'You do not have permission to access this page'
            )
            return redirect(reverse('product_all'))


def newsletter_delete(request, pk):
    profile_id = request.user.pk
    recipient = get_object_or_404(Newsletter, pk=pk)
    recipient.delete()
    messages.success(request, "Successfully unsubscribed.")
    return redirect('profile_detail', profile_id)


def newsletter_list(request):
    query = Profile.objects.all()
    profile_id = request.user.pk
    profile = get_object_or_404(query, auth_user_id=profile_id)
    recipients = Newsletter.objects.all().order_by('-subscribed_on')
    context = {
        'recipients': recipients,
        'profile': profile,
    }
    return render(
        request,
        'users/newsletter_list.html',
        context
    )
