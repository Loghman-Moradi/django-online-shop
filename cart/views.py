from django.shortcuts import render, get_object_or_404
from .cart import Cart
from shop.models import Product
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.http import Http404


@require_POST
def add_to_cart(request, product_id):
    try:
        product = get_object_or_404(Product, id=product_id)
        cart = Cart(request)
        cart.add(product)

        context = {
            'item_count': len(cart),
            'total_price': cart.get_total_price(),
        }

        return JsonResponse(context)
    except Http404:
        return JsonResponse({'error': 'Something went wrong'}, status=404)


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})


@require_POST
def update_quantity(request):
    action = request.POST['action']
    product_id = request.POST['product_id']

    try:
        product = get_object_or_404(Product, id=product_id)
        cart = Cart(request)

        if action == "add":
            cart.add(product)
        elif action == 'decrease':
            cart.decrease(product)

        product_cost = cart.cart[product_id]['quantity'] * cart.cart[product_id]['price']

        context = {
            'success': True,
            'item_count': len(cart),
            'total_price': cart.get_total_price(),
            'quantity': cart.cart[product_id]['quantity'],
            'product_cost': product_cost,
            'post_price': cart.get_post_price(),
            'final_price': cart.get_final_price(),
        }

        return JsonResponse(context)
    except Http404:
        return JsonResponse({'success': False, 'error': 'Something went wrong: product not found!'}, status=404)


def delete_product(request):
    product_id = request.POST['product_id']
    try:
        product = get_object_or_404(Product, id=product_id)
        cart = Cart(request)
        cart.remove(product)

        context = {
            'success': True,
            'item_count': len(cart),
            'total_price': cart.get_total_price(),
            'post_price': cart.get_post_price(),
            'final_price': cart.get_final_price(),
        }

        return JsonResponse(context)
    except Http404:
        return JsonResponse({'success': False, 'error': 'Something went wrong: product not found!'}, status=404)













