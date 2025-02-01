from django.shortcuts import render
from .models import FAQ, FAQCategory

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