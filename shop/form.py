from django import forms
from account.models import ShopUser


class UserRegisterForm(forms.ModelForm):
    class Meta:
        model = ShopUser
        fields = ('phone', 'first_name', 'last_name')