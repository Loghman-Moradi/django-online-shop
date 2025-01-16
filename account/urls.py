from django.urls import path
from . import views
app_name = 'account'

urlpatterns = [
    path('verify_phone/', views.verify_phone, name='verify_phone'),
    path('verify_code/', views.verify_code, name='verify_code'),
    path('log_out/', views.log_out, name='log_out'),
    path('profile/', views.profile, name="profile"),
    path('address/', views.address, name="address"),
    path('address_detail/<int:pk>/', views.address_detail, name="address_detail"),

    path('add_address/', views.add_address, name="add_address"),
    path('edit_address/<int:pk>/', views.edit_address, name="edit_address"),
    path('delete_address/<int:pk>/', views.delete_address, name="delete_address"),
    path('wishlist/', views.wishlist, name="wishlist"),
    path('toggle_wishlist/', views.toggle_wishlist, name="toggle_wishlist"),

]

