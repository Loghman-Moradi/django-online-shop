from django import forms
from .models import ShopUser, Address
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .validators import validate_unique_phone_number, phone_number_validator


class ShopUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = ShopUser
        fields = ('phone', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser', 'date_joined')

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        validate_unique_phone_number(phone)
        return phone


class ShopUserChangeForm(UserChangeForm):
    class Meta(UserCreationForm.Meta):
        model = ShopUser
        fields = ('phone', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser', 'date_joined')

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        validate_unique_phone_number(phone, self.instance.id)
        return phone


class PhoneVerificationForm(forms.Form):
    phone_number = forms.CharField(max_length=11, validators=[phone_number_validator])

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        validate_unique_phone_number(phone_number)
        return phone_number


class EditInformationForm(forms.ModelForm):
    class Meta:
        model = ShopUser
        fields = ['first_name', 'last_name']


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['first_name', 'last_name', 'phone_number', 'province', 'city', 'plate', 'unit', 'postal_code',
                  'address_line']

















