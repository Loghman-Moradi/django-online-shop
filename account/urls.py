from django.urls import path
from . import views
app_name = 'account'

urlpatterns = [
    path('verify_phone/', views.verify_phone, name='verify_phone'),
    path('verify_code/', views.verify_code, name='verify_code'),
]