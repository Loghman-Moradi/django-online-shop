import random
from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .common.kave_sms import send_sms_with_template, send_sms_normal
from .form import *
from .models import ShopUser


def verify_phone(request):
    if request.method == "POST":
        form = PhoneVerificationForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone_number']

            code = ''.join(random.sample('1234567890', 6))
            tokens = {'token': code}

            request.session['verification_code'] = code
            request.session['phone'] = phone

            send_sms_with_template(phone, tokens, 'user-login')
            messages.success(request, 'Your verification code has been sent.')
            return redirect('account:verify_code')
    else:
        form = PhoneVerificationForm()

    context = {
        'form': form
    }
    return render(request, 'form/verify_phone.html', context)


def verify_code(request):
    if request.method == "POST":
        received_code = request.POST.get('code')
        if received_code:
            verification_code = request.session['verification_code']
            phone = request.session['phone']
            if received_code == verification_code:
                if ShopUser.objects.filter(phone=phone).exists():
                    user = ShopUser.objects.get(phone=phone)
                else:
                    character = "QWERTYUIOPASDFGHJKLZXCVBNM-0123456789-@_qwertyuiopasdfghjklzxcvbnm"
                    user_password = ''.join(random.sample(character, 8))

                    user = ShopUser.objects.create_user(phone=phone)
                    user.set_password(user_password)
                    user.save()

                login(request, user)
                del request.session[verification_code]
                del request.session['phone']
        else:
            messages.success(request, 'Your verification code has been sent.')
    return redirect('shop:products')


























# def verify_phone(request):
#     if request.method == "POST":
#         form = PhoneVerificationForm(request.POST)
#         if form.is_valid():
#             phone = form.cleaned_data.get('phone_number')
#
#             code = ''.join(random.sample("0123456789", 6))
#             tokens = {'token': code}
#
#             request.session['verification_code'] = code
#             request.session['phone'] = phone
#
#             send_sms_with_template(phone, tokens, 'user-login')
#             messages.success(request, 'Your verification code has been sent.')
#             return redirect('account:verify_code')
#     else:
#         form = PhoneVerificationForm()
#     context = {
#         'form': form,
#     }
#     return render(request, 'form/verify_phone.html', context)
#
#
# def verify_code(request):
#     if request.method == "POST":
#         received_code = request.POST.get('code')
#         if received_code:
#             verification_code = request.session['verification_code']
#             phone = request.session['phone']
#
#             if received_code == verification_code:
#                 if ShopUser.objects.filter(phone=phone).exists():
#                     user = ShopUser.objects.get(phone=phone)
#                 else:
#                     character = 'QWERTYUIOPASDFGHJKLZXCVBNM-0123456789-@_qwertyuiopasdfghjklzxcvbnm'
#                     user_password = ''.join(random.sample(character, 8))
#
#                     user = ShopUser.objects.create_user()
#                     user.set_password(user_password)
#                     user.save()
#
#                 login(request, user)
#
#                 del request.session['verification_code']
#                 del request.session['phone']
#
#                 return redirect('shop:products')
#         else:
#             messages.error(request, 'Your verification code does not match.')
#     return render(request, 'form/verify_code.html')
#

