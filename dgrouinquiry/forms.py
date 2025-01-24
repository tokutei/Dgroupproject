# dgroupinquiry/forms.py
from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message', 'postal_code', 'address']  # 順番を逆に
