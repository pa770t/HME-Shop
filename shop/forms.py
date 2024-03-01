from django import forms
from .models import ShippingAddress, Payment, ContactInfo, PromoCode


class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['name', 'street_address', 'city', 'state', 'zip_code', 'country', 'email', 'phone_number']

    def clean_zip_code(self):
        data = self.cleaned_data["zip_code"]
        return data
    

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['name_on_card', 'card_number', 'expiry', 'cvc']

class ContactInfoForm(forms.ModelForm):
    class Meta:
        model = ContactInfo
        fields = ['first_name', 'last_name', 'email', 'message']

class PromoCodeForm(forms.ModelForm):
    class Meta:
        model = PromoCode
        fields = ['code']
