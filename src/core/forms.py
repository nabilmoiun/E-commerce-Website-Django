from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

CHOICE_FIELDS = (
    ('S', 'Stripe'),
    ('P', 'Paypal')
)


class CheckoutForm(forms.Form):
    street_adress = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': '1234 Main St',
    }))
    apartment_address = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Apartment or suite'
    }))
    country = CountryField(blank_label='select country').formfield(
        widget=CountrySelectWidget,
        attrs={
            'class': 'custom-select d-block w-100'
        }
    )
    zip_code = forms.CharField(widget=forms.TextInput())
    same_billing_address = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    save_info = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICE_FIELDS)

