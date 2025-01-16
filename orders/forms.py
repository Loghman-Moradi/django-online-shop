from django import forms
from .models import Order, ReturnedProducts
from account.models import Address


class PhoneVerificationPhone(forms.Form):
    phone_number = forms.CharField(max_length=11)

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']

        if not phone_number.isdigit():
            raise forms.ValidationError("Phone number must be digit")
        if len(phone_number) != 11:
            raise forms.ValidationError("Phone number must be 11 digits")
        if not phone_number.startswith('09'):
            raise forms.ValidationError("Phone number must start with 09")
        return phone_number


class ReturnedForm(forms.ModelForm):
    class Meta:
        model = ReturnedProducts
        fields = ['return_reason', 'image']

    def __init__(self, *args, **kwargs):
        order_item = kwargs.pop('order_item', None)
        super().__init__(*args, **kwargs)
        if order_item:
            self.fields['order_item'].initial = order_item
            self.fields['order_item'].widget = forms.HiddenInput()

















