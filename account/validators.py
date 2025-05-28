from django.core.validators import RegexValidator
from django.forms import ValidationError

phone_number_validator = RegexValidator(
    regex=r'^09\d{9}$',
    message='Phone number must start with "09"'
)


def validate_unique_phone_number(phone_number, exclude_id=None):
    from account.models import ShopUser
    qs = ShopUser.objects.filter(phone=phone_number)
    if exclude_id:
        qs = qs.exclude(id=exclude_id)
        if qs.exists():
            raise ValidationError("This phone number is already taken.")
