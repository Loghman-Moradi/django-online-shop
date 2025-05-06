from django import forms
from .models import ShopUser, Address
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class ShopUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = ShopUser
        fields = ('phone', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser', 'date_joined')

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if ShopUser.objects.filter(phone=phone).exists():
            raise forms.ValidationError("This phone number is already taken")
        if not phone.isdigit():
            raise forms.ValidationError("Phone number is invalid")
        if len(phone) != 11:
            raise forms.ValidationError("Phone number must have 11 digits")
        if not phone.startswith('09'):
            raise forms.ValidationError("Phone number must start with '09'")
        return phone


class ShopUserChangeForm(UserChangeForm):
    class Meta(UserCreationForm.Meta):
        model = ShopUser
        fields = ('phone', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser', 'date_joined')

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if ShopUser.objects.exclude(id=self.instance.id).filter(phone=phone).exists():
            raise forms.ValidationError("This phone number is already taken")
        if not phone.isdigit():
            raise forms.ValidationError("Phone number is invalid")
        if len(phone) != 11:
            raise forms.ValidationError("Phone number must have 11 digits")
        if not phone.startswith('09'):
            raise forms.ValidationError('Phone number must start with "09"')
        return phone


class PhoneVerificationForm(forms.Form):
    phone_number = forms.CharField(max_length=11, error_messages={
            'max_length': 'Phone number must have 11 digits',
        })

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')

        if not phone_number.isdigit():
            raise forms.ValidationError("Phone number is invalid")
        if len(phone_number) != 11:
            raise forms.ValidationError("Phone number must have 11 digits")
        if not phone_number.startswith('09'):
            raise forms.ValidationError("Phone number must start with '09'")
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

















