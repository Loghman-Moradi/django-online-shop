from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path("products/", views.product_list, name="products"),
    path("products/sort/<slug:sort_slug>/", views.product_list, name="product_by_sort"),
    path("product_detail/<int:id>/<slug:slug>/", views.product_detail, name="product_detail"),
    path("search/", views.search, name="search"),


]