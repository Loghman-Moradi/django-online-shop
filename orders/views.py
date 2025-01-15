import os
from bidi.algorithm import get_display
from arabic_reshaper import reshape
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404, Http404
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from account.form import AddressForm
from .forms import *
from account.common.kave_sms import send_sms_with_template
from cart.cart import Cart
from .models import *
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import redirect
from django.http import HttpResponse
import requests
import json
from shop.utils import verify_phone_base, verify_code_base


def verify_phone(request):
    return verify_phone_base(request, PhoneVerificationPhone, 'orders/verify_phone.html', 'orders:verify_code')


def verify_code(request):
    return verify_code_base(request, 'orders:order_create')



@login_required
def order_create(request):
    addresses = Address.objects.filter(user=request.user)
    has_address = addresses.exists()
    cart = Cart(request)
    if request.method == 'POST':
        if 'selected_address' in request.POST:
            selected_address_id = request.POST.get('selected_address')
            selected_address = Address.objects.get(id=selected_address_id)
            order = Order.objects.create(
                buyer=request.user,
            )

            OrderAddress.objects.create(
                order=order,
                address=selected_address,
            )

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'],
                    weight=item['weight'],
                )
            cart.clear()
            request.session['order_id'] = order.id
            return redirect('orders:request')
        else:
            form = AddressForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                address = Address.objects.create(
                  user=request.user,
                  first_name=cd['first_name'],
                  last_name=cd['last_name'],
                  phone_number=cd['phone_number'],
                  province=cd['province'],
                  city=cd['city'],
                  postal_code=cd['postal_code'],
                  unit=cd['unit'],
                  plate=cd['plate'],
                  address_line=cd['address_line'],
              )
                order = Order.objects.create(
                    buyer=request.user,
                )

                OrderAddress.objects.create(
                    order=order,
                    address=address
                )

                for item in cart:
                    OrderItem.objects.create(
                        order=order,
                        product=item['product'],
                        price=item['price'],
                        quantity=item['quantity'],
                        weight=item['weight'],
                    )

                cart.clear()
                request.session['order_id'] = order.id
                return redirect('orders:request')
    else:
        form = AddressForm()
    context = {
        'form': form,
        'addresses': addresses,
        'has_address': has_address,
        'cart': cart,
    }
    return render(request, 'orders/order_create.html', context)


#? sandbox merchant
if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'


ZP_API_REQUEST = "https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = "https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = "https://sandbox.zarinpal.com/pg/StartPay/"


amount = 1000
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"
phone = 'YOUR_PHONE_NUMBER'
CallbackURL = 'http://127.0.0.1:8000/order/verify/'


def send_request(request):
    order = Order.objects.get(id=request.session['order_id'])
    description = ""
    for item in order.items.all():
        description += item.product.name + ", "
    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": order.get_final_cost(),
        "Description": description,
        "Phone": request.user.phone,
        "CallbackURL": CallbackURL,


    }
    data = json.dumps(data)
    headers = {'accept': 'application/json', 'content-type': 'application/json', 'content-length': str(len(data))}
    try:
        response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)

        if response.status_code == 200:
            response_json = response.json()
            authority = response_json.get('Authority')
            if response_json.get('Status') == 100:
                return redirect(ZP_API_STARTPAY + authority)
            else:
                return HttpResponse(f"Error: {response_json.get('Status')}")
        return HttpResponse(f"response failed: {response.status_code}")
    except requests.exceptions.Timeout:
        return HttpResponse('Timeout Error')
    except requests.exceptions.ConnectionError:
        return HttpResponse('Connection Error')


def verify(request):
    order = Order.objects.get(id=request.session['order_id'])
    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": order.get_final_cost(),
        "Authority": request.GET.get('Authority'),
    }
    data = json.dumps(data)
    headers = {'accept': 'application/json', 'content-type': 'application/json', 'content-length': str(len(data))}
    try:
        response = requests.post(ZP_API_VERIFY, data=data, headers=headers)
        if response.status_code == 200:
            response_json = response.json()
            reference_id = response_json['RefID']
            if response_json['Status'] == 100:
                for item in order.items.all():
                    item.product.inventory -= item.quantity
                    item.product.save()
                order.paid = True
                order.save()
                return render(request, 'orders/payment-tracking.html',
                              {'success': True, 'RefID': reference_id, 'order_id': order.id})
            else:
                return render(request, 'orders/payment-tracking.html',
                              {'success': False, })
        del request.session['order_id']
        return HttpResponse('response failed')
    except requests.exceptions.Timeout:
        return HttpResponse('Timeout Error')
    except requests.exceptions.ConnectionError:
        return HttpResponse('Connection Error')


def order_list(request, status=None):
    user = request.user
    if status:
        orders = Order.objects.filter(buyer=user, status=status)
    else:
        orders = Order.objects.filter(buyer=user)

    context = {
        'orders': orders,
        'status': status,
    }
    return render(request, 'orders/order_list.html', context)


def order_detail(request, order_id):
    try:
        order = get_object_or_404(Order, id=order_id, buyer=request.user)
    except Http404:
        raise Http404()
    order_items = OrderItem.objects.filter(order=order)
    context = {
        'order': order,
        'order_items': order_items,
    }

    return render(request, 'orders/order_detail.html', context)


def order_invoice(request, order_id):
    try:
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        return HttpResponse("order not found")

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice_{}.pdf"'.format(order_id)
    p = canvas.Canvas(response, pagesize=letter)
    p.drawString(100, 750, "order invoice")
    p.drawString(100, 730, f"order number: {order.id}")
    p.drawString(100, 710, f"order date: {order.created_at}")
    p.drawString(100, 690, f"Name of the buyer: {order.buyer}")

    y_pos = 650
    for item in OrderItem.objects.filter(order=order):
        p.drawString(100, y_pos, f"product: {item.product.name}")
        p.drawString(300, y_pos, f"price: {item.price}")
        p.drawString(400, y_pos, f"number: {item.quantity}")
        y_pos -= 20

    p.drawString(100, y_pos - 20, f"total amount: {order.get_total_cost()}")
    p.drawString(100, y_pos - 40, f"----------------------------------")
    p.drawString(100, y_pos - 60, "market: liashopstar")
    p.drawString(100, y_pos - 80, "phone shop: 09214249950")

    p.save()
    return response


def return_product(request, item_id):
    order_item = get_object_or_404(OrderItem, id=item_id)

    if request.method == 'POST':
        form = ReturnedForm(request.POST, request.FILES)
        if form.is_valid():
            returned_product = form.save(commit=False)
            returned_product.order_item = order_item
            returned_product.user = request.user  # فرض بر این است که کاربر لاگین کرده است
            returned_product.save()
            # می‌توانید کارهایی مثل ریدایرکت یا نمایش پیام موفقیت انجام دهید
    else:
        form = ReturnedForm(order_item=order_item)

    return render(request, 'orders/return_product.html', {'form': form, 'order_item': order_item})










