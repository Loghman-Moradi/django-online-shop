from shop.models import Product
from django.conf import settings


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart
        self.cart.update()

    def add(self, product):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 1, 'price': product.new_price, 'weight': product.weight}
        else:
            if self.cart[product_id]['quantity'] < product.inventory:
                self.cart[product_id]['quantity'] += 1
        self.save()

    def decrease(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            if self.cart[product_id]['quantity'] > 1:
                self.cart[product_id]['quantity'] -= 1
            self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        del self.session['cart']
        self.save()

    def update_price(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            product_id = str(product.id)
            if product_id in self.cart:
                self.cart[product_id]['price'] = product.new_price

    def get_post_price(self):
        weight = sum(item['weight'] * item['quantity'] for item in self.cart.values())
        if weight < settings.SHIPPING_COSTS['TIER1_MAX_WEIGHT'] + 1:
            return settings.SHIPPING_COSTS['TIER1_COST']
        elif weight < settings.SHIPPING_COSTS['TIER2_MAX_WEIGHT'] + 1:
            return settings.SHIPPING_COSTS['TIER2_COST']
        else:
            return settings.SHIPPING_COSTS['TIER3_COST']

    def get_total_price(self):
        self.update_price()
        priced = sum(item['price'] * item['quantity'] for item in self.cart.values())
        return priced

    def get_final_price(self):
        return self.get_total_price() + self.get_post_price()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart_dict = self.cart.copy()
        for product in products:
            cart_dict[str(product.id)]['product'] = product
        for item in cart_dict.values():
            item['total'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def save(self):
        self.session.modified = True

