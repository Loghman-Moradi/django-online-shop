from datetime import timedelta, timezone
from django.db import transaction
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, Http404
from django.views.decorators.csrf import csrf_exempt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from account.forms import AddressForm
from .forms import PhoneVerificationPhone, ReturnedForm
from cart.cart import Cart
from .models import Address, Order, OrderAddress, OrderItem
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


@login_required(login_url='orders:verify_phone')
def order_create(request):
    addresses = Address.objects.filter(user=request.user)
    has_address = addresses.exists()
    cart = Cart(request)

    if request.method == 'POST':
        with transaction.atomic():
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
                return redirect('orders:request_payment', order_id=order.id)

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
                    return redirect('orders:request_payment', order_id=order.id)
                else:
                    messages.error(request, 'لطفاً اطلاعات آدرس جدید را به درستی وارد کنید.')
                    context = {
                        'form': form,
                        'addresses': addresses,
                        'has_address': has_address,
                        'cart': cart,
                    }
                    return render(request, 'orders/order_create.html', context)
    else:
        form = AddressForm()

    context = {
        'form': form,
        'addresses': addresses,
        'has_address': has_address,
        'cart': cart,
    }
    return render(request, 'orders/order_create.html', context)


def request_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, buyer=request.user, paid=False)

    amount_rial = order.get_total_cost()
    user_mobile = request.user.phone if hasattr(request.user, 'phone') and request.user.phone else ''
    user_email = request.user.email if hasattr(request.user, 'email') and request.user.email else ''

    data = {
        'pin': settings.AQAYEPARDAKHT_PIN,
        'amount': amount_rial,
        'callback': settings.AQAYEPARDAKHT_CALLBACK_URL,
        'card_number': '',
        'mobile': user_mobile,
        'email': user_email,
        'invoice_id': str(order.id),
        'description': f'پرداخت فاکتور شماره {order.id} از فروشگاه شما'
    }

    try:
        response = requests.post(settings.AQAYEPARDAKHT_CREATE_URL, data=data)
        json_data = response.json()

        if response.status_code == 200 and json_data.get('status') == 'success':
            start_pay_url = settings.AQAYEPARDAKHT_STARTPAY_URL + json_data.get('transid')
            return redirect(start_pay_url)
        else:
            error_message = json_data.get('code') or json_data.get('message', 'خطای ناشناخته در ایجاد تراکنش')
            messages.error(request, f'خطا در شروع پرداخت: {error_message}')
            return redirect('orders:order_detail', order_id=order.id)

    except requests.exceptions.RequestException as e:
        messages.error(request, f'خطا در ارتباط با درگاه پرداخت: {e}')
        return redirect('orders:order_detail', order_id=order.id)
    except json.JSONDecodeError:
        messages.error(request, 'خطا در خواندن پاسخ درگاه پرداخت.')
        return redirect('orders:order_detail', order_id=order.id)


@csrf_exempt
def confirm_payment(request):
    transid = request.POST.get('transid')
    status = request.POST.get('status')
    amount_paid_str = request.POST.get('amount')
    invoice_id = request.POST.get('invoice_id')

    print(f"Raw POST data: {request.POST}")
    if not transid or not status or not invoice_id:
        messages.error(request, 'اطلاعات پرداخت ناقص است.')
        return redirect('orders:order_list')

    try:
        order = get_object_or_404(Order, id=invoice_id)
        amount_paid = int(amount_paid_str) if amount_paid_str else order.get_total_cost()
    except ValueError:
        messages.error(request, 'مبلغ برگشتی از درگاه نامعتبر است.')
        return redirect('orders:order_list')
    except Order.DoesNotExist:
        messages.error(request, 'سفارش مورد نظر یافت نشد.')
        return redirect('orders:order_list')

    if status == 'success' or status == '1':
        data = {
            'pin': settings.AQAYEPARDAKHT_PIN,
            'amount': amount_paid,
            'transid': transid
        }

        print(f"Sending verification request to {settings.AQAYEPARDAKHT_VERIFY_URL} with data: {data}")

        try:
            response = requests.post(settings.AQAYEPARDAKHT_VERIFY_URL, data=data)
            json_data = response.json()
            print(f"Verification response: {json_data}")

            if response.status_code == 200 and json_data.get('code') == '1':
                if amount_paid == order.get_total_cost():
                    order.paid = True
                    order.status = 'COMPLETED'
                    order.save()

                    messages.success(request, 'پرداخت با موفقیت انجام شد و سفارش شما ثبت گردید.')
                    return redirect('orders:order_detail', order_id=order.id)
                else:
                    messages.error(request,
                                   'مبلغ پرداخت شده با مبلغ سفارش مطابقت ندارد. لطفاً با پشتیبانی تماس بگیرید.')
                    order.status = 'PAYMENT_FAILED_AMOUNT_MISMATCH'
                    order.save()
                    return redirect('orders:order_detail', order_id=order.id)
            else:

                error_message = json_data.get('message',
                                              f'خطای ناشناخته در تأیید پرداخت. کد: {json_data.get("code", "نامشخص")}')
                messages.error(request, f'تراکنش تأیید نشد: {error_message}')
                order.status = 'PAYMENT_VERIFICATION_FAILED'
                order.save()
                return redirect('orders:order_detail', order_id=order.id)

        except requests.exceptions.RequestException as e:
            messages.error(request, f'خطا در ارتباط با درگاه پرداخت در مرحله تأیید: {e}')
            order.status = 'PAYMENT_VERIFICATION_ERROR'
            order.save()
            return redirect('orders:order_detail', order_id=order.id)
        except json.JSONDecodeError:
            messages.error(request, 'خطا در خواندن پاسخ تأیید درگاه پرداخت.')
            order.status = 'PAYMENT_VERIFICATION_ERROR'
            order.save()
            return redirect('orders:order_detail', order_id=order.id)

    else:
        messages.error(request, 'پرداخت توسط شما لغو شد یا ناموفق بود.')
        order.status = 'CANCELLED'
        order.save()
        return redirect('orders:order_detail', order_id=order.id)


def order_list(request, status=None):
    user = request.user
    orders_queryset = Order.objects.select_related('order__address', 'buyer').prefetch_related('items__product')
    if status:
        orders = orders_queryset.filter(buyer=user, status=status)
    else:
        orders = orders_queryset.filter(buyer=user)

    context = {
        'orders': orders,
        'status': status,
    }
    return render(request, 'orders/order_list.html', context)


def order_detail(request, order_id):
    try:
        order = get_object_or_404(
            Order.objects.select_related('order__address', 'buyer').prefetch_related('items__product'),
            id=order_id,
            buyer=request.user
        )
    except Http404:
        raise Http404()
    order_items = order.items.all()
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
    p.drawString(100, y_pos - 80, "phone shop: ************")

    p.save()
    return response


@login_required
def return_product(request, item_id):
    order_item = get_object_or_404(OrderItem, id=item_id)
    can_return = False

    if order_item.order.status == "DELIVERED":
        if order_item.order.delivery_date:
            time_difference = timezone.now() - order_item.order.delivery_date
            if time_difference <= timedelta(days=7):
                can_return = True

    if request.method == 'POST':
        form = ReturnedForm(request.POST, request.FILES)
        if form.is_valid():
            returned_product = form.save(commit=False)
            returned_product.order_item = order_item
            returned_product.user = request.user
            returned_product.save()
            messages.success(request, 'Your request has been successfully registered.')
        else:
            messages.error(request, 'Something went wrong. Please try again.')

    else:
        form = ReturnedForm()
    context = {
        'order_item': order_item,
        'form': form,
        'can_return': can_return,
    }

    return render(request, 'orders/return_product.html', context)
