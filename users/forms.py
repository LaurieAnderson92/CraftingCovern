from django import forms
from .models import Newsletter

class NewsletterSignupForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['email','profile']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile'].widget.attrs['type'] = 'hidden'