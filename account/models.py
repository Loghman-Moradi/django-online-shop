from django.utils import timezone
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.


class ShopUserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError('Users must have a phone')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, phone, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone, password, **extra_fields)


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='addresses', blank=True, null=True)
    first_name = models.CharField(max_length=20, blank=False, null=False)
    last_name = models.CharField(max_length=20, blank=False, null=False)
    phone_number = models.CharField(max_length=11, blank=False, null=False)
    province = models.CharField(max_length=20, blank=False, null=False)
    city = models.CharField(max_length=20, blank=False, null=False)
    plate = models.CharField(max_length=10, blank=False, null=False)
    unit = models.CharField(max_length=10, blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=False, null=False)
    address_line = models.TextField(blank=False, null=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.address_line}, {self.city}"

    class Meta:
        ordering = ['-address_line']
        indexes = [
            models.Index(fields=['-address_line'])
        ]

        verbose_name = "آدرس"
        verbose_name_plural = "آدرس ها"


class ShopUser(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=11, unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = ShopUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone















