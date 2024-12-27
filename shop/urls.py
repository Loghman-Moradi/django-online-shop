from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path("products/", views.products, name="products"),
    path("product_detail/<int:id>/<slug:slug>/", views.product_detail, name="product_detail"),

]