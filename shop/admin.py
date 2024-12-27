from django.contrib import admin

from shop.models import *


class ProductFeaturesInline(admin.TabularInline):
    model = ProductFeatures
    extra = 1

class ImageInline(admin.TabularInline):
    model = Images
    extra = 1


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'inventory', 'new_price', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['name', 'description']
    inlines = [ProductFeaturesInline, ImageInline]
