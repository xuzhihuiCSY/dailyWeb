from django import forms
from django.contrib.auth.models import User

from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_name', 'customer_email', 'shipping_address', 'billing_address']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['customer_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['customer_email'].widget.attrs.update({'class': 'form-control'})
        self.fields['shipping_address'].widget.attrs.update({'class': 'form-control'})
        self.fields['billing_address'].widget.attrs.update({'class': 'form-control'})
