import random
from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from .form import *
from django.contrib.auth.decorators import login_required
from shop.utils import verify_code_base, verify_phone_base


def verify_phone(request):
    return verify_phone_base(request, PhoneVerificationForm, 'form/verify_phone.html', 'account:verify_code')


def verify_code(request):
    return verify_code_base(request, 'shop:products')


def log_out(request):
    logout(request)
    return redirect('account:verify_phone')


@login_required
def profile(request):
    user = request.user
    return render(request, 'form/profile.html', {'user': user})


@login_required
def address(request):
    user = request.user
    my_address = Address.objects.filter(user=user)
    context = {
        'my_address': my_address,
    }
    return render(request, 'form/my_address.html', context)


@login_required
def add_address(request):
    if request.method == "POST":
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

            address.save()
            messages.success(request, 'Your address has been added.')
    else:
        form = AddressForm()
    context = {
        'form': form,
    }
    return render(request, 'form/address_form.html', context)


def address_detail(request, pk):
    my_address = get_object_or_404(Address, pk=pk, user=request.user)
    context = {
        'my_address': my_address,
    }

    return render(request, 'form/address_detail.html', context)


def edit_address(request, pk):
    address = get_object_or_404(Address, pk=pk, user=request.user)
    if request.method == "POST":
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your address has been updated.')
    else:
        form = AddressForm(instance=address)
    context = {
        'form': form,
        'address': address,
    }
    return render(request, 'form/edit_address.html', context)


def delete_address(request, pk):
    address = get_object_or_404(Address, pk=pk, user=request.user)
    address.delete()
    return redirect('account:address')










