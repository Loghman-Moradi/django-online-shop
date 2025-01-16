from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from account.models import ShopUser


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام")
    slug = models.SlugField(unique=True, verbose_name="اسلاگ")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(str(self.name))
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]

        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100, verbose_name="نام")
    slug = models.SlugField(unique=True, verbose_name="اسلاگ")
    description = models.TextField(verbose_name="توضیحات")
    inventory = models.PositiveIntegerField(default=0, verbose_name="موجودی")
    weight = models.PositiveIntegerField(default=0, verbose_name="وزن")
    price = models.PositiveIntegerField(default=0, verbose_name="قیمت")
    offers = models.PositiveIntegerField(default=0, verbose_name="تخفیف")
    new_price = models.PositiveIntegerField(default=0, verbose_name="قیمت پس از تخفیف")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created_at']),
        ]

        verbose_name = "محصول"
        verbose_name_plural = "محصولات"

    def get_absolute_url(self):
        return reverse('shop:product_detail', kwargs={'id': self.id, 'slug': self.slug})

    def __str__(self):
        return f"{self.name}:"


class ProductFeatures(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام")
    value = models.CharField(max_length=255, verbose_name="ویژگی")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='features')

    class Meta:
        ordering = ['name']

        verbose_name = "ویژگی"
        verbose_name_plural = "ویژگی ها"

    def __str__(self):
        return f"{self.name}:{self.value}"


class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image_file = models.ImageField(upload_to='product_image/%y/%m/%d')
    title = models.CharField(max_length=100, verbose_name="عنوان", blank=True)
    description = models.TextField(verbose_name="توضیحات", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
        ]

        verbose_name = "تصاویر"
        verbose_name_plural = "تصاویر ها"

    def __str__(self):
        return f"{self.title}" if self.title else f"{self.image_file}"


















