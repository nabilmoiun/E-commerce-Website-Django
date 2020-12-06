from django import forms

from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

from .models import Comment

CHOICE_FIELDS = (
    ('S', 'Stripe'),
    ('P', 'Paypal'),
    ('SSL', 'SSL Ecommerce')
)


class CheckoutForm(forms.Form):
    # Shipping information
    shipping_address = forms.CharField(required=False)
    shipping_address2 = forms.CharField(required=False)
    shipping_country = CountryField(blank_label='(select country)').formfield(
        required=False,
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100',
        }))
    shipping_zip = forms.CharField(required=False)
    same_billing_address = forms.BooleanField(required=False)
    set_default_shipping = forms.BooleanField(required=False)
    use_default_shipping = forms.BooleanField(required=False)

    # Billing information
    billing_address = forms.CharField(required=False)
    billing_address2 = forms.CharField(required=False)
    billing_country = CountryField(blank_label='(select country)').formfield(
        required=False,
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100',
        }))
    billing_zip = forms.CharField(required=False)
    set_default_billing = forms.BooleanField(required=False)
    use_default_billing = forms.BooleanField(required=False)

    # Payment Method
    payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICE_FIELDS)


class CouponForm(forms.Form):
    coupon_code = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control",
        'placeholder': 'Promo Code',
        'aria-label': 'Recipient\'s username',
        'aria-describedby':"basic-addon2"
        }
    ))


class RefundForm(forms.Form):
    reference_code = forms.CharField(max_length=20)
    reason = forms.CharField(widget=forms.Textarea(attrs={
        "row": 2
    }))
    email = forms.EmailField()


class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(attrs={
        "cols": 200,
        "rows": 3,
        "class": "form-control",
        "placeholder": "Write A Comment"
    }))
