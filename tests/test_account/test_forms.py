from django.test import TestCase
from account.form import PhoneVerificationForm, ShopUserCreationForm
from account.models import ShopUser


class PhoneVerificationFormTest(TestCase):

    def test_valid_phone_number(self):
        form = PhoneVerificationForm(data={'phone_number': "09123456789"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['phone_number'], "09123456789")

    def test_empty_data(self):
        form = PhoneVerificationForm(data={'phone_number': ""})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_phone_number_not_digits(self):
        form = PhoneVerificationForm(data={"phone_number": "0912A@l6789"})
        self.assertFalse(form.is_valid())
        self.assertIn('phone_number', form.errors)
        self.assertEqual(form.errors['phone_number'], ['Phone number is invalid'])

    def test_phone_number_length_invalid(self):
        form = PhoneVerificationForm(data={'phone_number': "0912345678"})
        self.assertFalse(form.is_valid())
        self.assertIn('phone_number', form.errors)
        self.assertEqual(form.errors['phone_number'], ["Phone number must have 11 digits"])

        form = PhoneVerificationForm(data={'phone_number': "091234567890"})
        self.assertFalse(form.is_valid())
        self.assertIn('phone_number', form.errors)
        self.assertEqual(form.errors['phone_number'], ["Phone number must have 11 digits"])

    def test_phone_number_does_not_start_with_09(self):
        form = PhoneVerificationForm(data={'phone_number': "77123456789"})
        self.assertFalse(form.is_valid())
        self.assertIn('phone_number', form.errors)
        self.assertEqual(form.errors['phone_number'], ["Phone number must start with '09'"])
#

















