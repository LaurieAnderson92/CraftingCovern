from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from .models import FAQ, FAQCategory, Contact
from .forms import ContactForm
from django.core.mail import send_mail

def faq_view(request):
    categories = FAQCategory.objects.all()
    faqs = FAQ.objects.all()
    template = 'help/faq.html'
    
    try:
        profile = get_object_or_404(query, auth_user_id=profile_id)
        context = {
            'categories': categories,
            'faqs': faqs,
            'profile':profile,
        }
    except:
        context = {
            'categories': categories,
            'faqs': faqs,
        }
    return render(request, template, context)


def contact_view(request):
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            from_email = settings.EMAIL_HOST_USER
            to_email = settings.EMAIL_HOST_USER
            contact_request = contact_form.save()
            messages.success(request, 
                           'Thank you for contacting us! We will get back to you soon.')
            subject = f'Contact Request:{contact_request.id}'
            body = f'''Someone has reached out via the online form:
                Name:{contact_request.name}
                Email:{contact_request.email}
                Phone:{contact_request.phone}
                Message:{contact_request.message}
                '''
            send_mail(
                subject,
                body,
                from_email,
                [to_email]
            )            
            return redirect('product_all')
    else:
        contact_form = ContactForm()
        template = 'help/contact.html'
    
    try:
        profile = get_object_or_404(query, auth_user_id=profile_id)
        context = {
            'profile': profile,
            'contact_form': contact_form,
        }
    except:
        context = {
            'contact_form': contact_form,
        }
    return render(request, template, context)