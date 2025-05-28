from django.urls import path
from . import views
app_name = 'orders'


urlpatterns = [
    path('verify_phone/', views.verify_phone, name='verify_phone'),
    path('verify_code/', views.verify_code, name='verify_code'),
    path('order_create/', views.order_create, name='order_create'),
    # path('request/', views.send_request, name='request'),
    # path('verify/', views.verify, name='verify'),
    path('request-payment/<int:order_id>/', views.request_payment, name='request_payment'),
    path('confirm-payment/', views.confirm_payment, name='confirm_payment'),
    path('order_list/', views.order_list, name='order_list'),
    path('order_list/<str:status>/', views.order_list, name='order_by_status'),
    path('order_detail/<int:order_id>/', views.order_detail, name='order_detail'),
    path('order/<int:order_id>/invoice/', views.order_invoice, name='order_invoice'),
    path('return_product/<int:item_id>/', views.return_product, name='return_product'),


]

