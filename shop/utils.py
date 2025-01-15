from datetime import datetime
from datetime import timedelta
import random
from django.contrib import messages
from django.contrib.auth import login
from django.utils import timezone
from account.common.kave_sms import send_sms_with_template
from django.shortcuts import redirect, render
from account.models import ShopUser


def verify_phone_base(request, phone_form, template_name, redirect_url):
    if request.method == 'POST':
        form = phone_form(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone_number']
            code = ''.join(random.sample("0123456789", 6))
            tokens = {'token': code}
            print(tokens)
            request.session['verification_code'] = code
            request.session['phone'] = phone
            request.session['code_generated_time'] = timezone.now().isoformat()

            # send_sms_with_template(phone, tokens, 'user_login')
            messages.success(request, 'Your phone has been verified.')
            return redirect(redirect_url)
    else:
        form = phone_form()
    context = {
        'form': form
    }

    return render(request, template_name, context)


def verify_code_base(request, redirect_url):
    if request.method == 'POST':
        received_code = request.POST.get('code')
        if received_code:
            verification_code = request.session.get('verification_code')
            phone = request.session.get('phone')
            code_generated_time_str = request.session.get('code_generated_time')
            if code_generated_time_str:
                code_generated_time = timezone.datetime.fromisoformat(code_generated_time_str)

                if timezone.now() > code_generated_time + timedelta(minutes=2):
                    messages.error(request, 'Your verification code has expired.')
                    return render(request, 'form/verify_code.html')

                if received_code == verification_code:
                    if ShopUser.objects.filter(phone=phone).exists():
                        user = ShopUser.objects.get(phone=phone)
                    else:
                        character = 'QWERTYUIOPASDFGHJKLZXCVBNM-0123456789-@_qwertyuiopasdfghjklzxcvbnm'
                        user_password = ''.join(random.sample(character, 8))

                        user = ShopUser.objects.create_user(phone=phone)
                        user.set_password(user_password)
                        user.save()
                    login(request, user)
                    del request.session['verification_code']
                    del request.session['phone']
                    del request.session['code_generated_time']
                    return redirect(redirect_url)
                else:
                    messages.error(request, 'Your verification code does not match.')
    return render(request, 'form/verify_code.html')




















