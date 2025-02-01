from django.urls import path
from . import views


urlpatterns = [
    path('faq/', views.faq_view, name='faq'),
    # path('contact/', views.contact_view, name='contact'),
    # path('contact/submit/', views.handle_contact_form, name='contact_submit'),
]