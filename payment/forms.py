from django import forms
from payment.models import BillingAddress
from order.models import Order


class BillingAddressForm(forms.ModelForm):
    class Meta:
        model = BillingAddress
        fields = ['first_name','last_name','address1','address2','country','city','zip_code','phone_number']


class PaymentMethodForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['payment_method',]