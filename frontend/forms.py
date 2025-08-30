from django import forms
from backend.models import Review, Order, ShippingAddress

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'title', 'message']

class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['address', 'city', 'region', 'phone']


class CheckoutForm(forms.Form):
    payment_method = forms.ChoiceField(
        choices=[('card', 'Credit/Debit Card'), ('paypal', 'PayPal')],
        widget=forms.RadioSelect
    )

