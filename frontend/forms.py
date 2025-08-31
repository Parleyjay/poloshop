from django import forms
from .models import Address, Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'subject', 'message']

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['street_name', 'country','city', 'region',]


# class CheckoutForm(forms.Form):
#     payment_method = forms.ChoiceField(
#         choices=[('card', 'Credit/Debit Card'), ('paypal', 'PayPal')],
#         widget=forms.RadioSelect
#     )

