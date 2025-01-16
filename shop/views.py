from django.shortcuts import render, get_object_or_404
from .form import SearchForm
from .models import *
from django.contrib.postgres.search import TrigramSimilarity


def product_list(request, category_slug=None, sort_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.all()

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    if sort_slug:
        if sort_slug == "newest":
            products = products.order_by('-created_at')
        elif sort_slug == "price_asc":
            products = products.order_by('price')
        elif sort_slug == "price_desc":
            products = products.order_by('-price')
        elif sort_slug == "biggest_discount":
            products = products.order_by('-offers')

    context = {
        'products': products,
        'category': category,
        'categories': categories,
    }

    return render(request, 'shop/product_list.html', context)


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug)
    similar_products = Product.objects.exclude(id=product.id).filter(name__icontains=product.name.split(' ')[0])[:5]
    context = {
        'product': product,
        'similar_products': similar_products,
    }
    return render(request, 'shop/product_detail.html', context)


def search(request):
    query = None
    result = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            result = Product.objects.annotate(similarity=TrigramSimilarity('name', query) +
                                              TrigramSimilarity('description', query))\
            .filter(similarity__gt=0.2).order_by('-similarity')

    context = {
        'query': query,
        'result': result,
    }

    return render(request, 'shop/search.html', context)










