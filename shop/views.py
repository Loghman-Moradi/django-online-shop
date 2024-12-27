from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import *
# Create your views here.


def products(request):
    products = Product.objects.all()
    context = {
        'products': products,
    }

    return render(request, 'shop/product_list.html', context)


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug)
    context = {
        'product': product,
    }
    return render(request, 'shop/product_detail.html', context)


# def register(request):
#     if request.method == 'POST':
#
#












