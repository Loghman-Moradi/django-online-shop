from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(str(self.name), allow_unicode=True)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]

        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    inventory = models.PositiveIntegerField(default=0)
    weight = models.PositiveIntegerField(default=0)
    price = models.PositiveIntegerField(default=0)
    offers = models.PositiveIntegerField(default=0)
    new_price = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created_at']),
        ]

        verbose_name = "product"
        verbose_name_plural = "products"

    def get_absolute_url(self):
        return reverse('shop:product_detail', kwargs={'id': self.id, 'slug': self.slug})

    def __str__(self):
        return f"{self.name}:"


class ProductFeatures(models.Model):
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='features')

    class Meta:
        ordering = ['name']

        verbose_name = "feature"
        verbose_name_plural = "features"

    def __str__(self):
        return f"{self.name}:{self.value}"


class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image_file = models.ImageField(upload_to='product_image/')
    title = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
        ]

        verbose_name = "image"
        verbose_name_plural = "images"

    def __str__(self):
        return f"{self.title}" if self.title else f"{self.image_file}"


















