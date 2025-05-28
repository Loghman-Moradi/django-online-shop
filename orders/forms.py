from django import forms
from .models import ReturnedProducts
from account.validators import phone_number_validator, validate_unique_phone_number


class PhoneVerificationPhone(forms.Form):
    phone_number = forms.CharField(max_length=11, validators=[phone_number_validator])

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        validate_unique_phone_number(phone_number)
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

















