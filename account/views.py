from django.contrib import messages
from django.contrib.auth import logout
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PhoneVerificationForm, AddressForm
from django.contrib.auth.decorators import login_required
from shop.utils import verify_code_base, verify_phone_base
from .models import Wishlist, Address
from shop.models import Product


def verify_phone(request):
    return verify_phone_base(
        request, PhoneVerificationForm, 'form/verify_phone.html', 'account:verify_code')


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
            Address.objects.create(
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

            messages.success(request, 'Your address has been added.')
    else:
        form = AddressForm()
    context = {
        'form': form,
    }
    return render(request, 'form/address_form.html', context)


@login_required
def address_detail(request, pk):
    my_address = get_object_or_404(Address, pk=pk, user=request.user)
    context = {
        'my_address': my_address,
    }

    return render(request, 'form/address_detail.html', context)


@login_required
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


@login_required
def delete_address(request, pk):
    address = get_object_or_404(Address, pk=pk, user=request.user)
    address.delete()
    return redirect('account:address')


@login_required
def wishlist(request):
    wishlist_item = Wishlist.objects.filter(user=request.user)
    products = [item.product for item in wishlist_item]
    context = {
        'products': products,
    }

    return render(request, 'form/wishlist.html', context)


def toggle_wishlist(request):
    product_id = request.POST.get('product_id')
    product = get_object_or_404(Product, pk=product_id)
    user_wishlist, created = Wishlist.objects.get_or_create(user=request.user, product=product)

    if not created:
        user_wishlist.delete()
        return JsonResponse({'status': 'removed'})
    else:
        return JsonResponse({'status': 'added'})













