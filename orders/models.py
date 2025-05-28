from django.db import models
from django.utils import timezone
from django_jalali.db import models as jmodels
from shop.models import Product
from account.models import ShopUser, Address


class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'در انتظار پرداخت'),
        ('PROCESSING', 'در حال پردازش'),
        ('SHIPPED', 'ارسال شده'),
        ('DELIVERED', 'تحویل داده شده'),
        ('CANCELLED', 'لغو شده'),
        ('RETURNED', 'مرجوع شده')
    ]
    buyer = models.ForeignKey(ShopUser, related_name='orders_buyer', on_delete=models.SET_NULL, null=True)
    paid = models.BooleanField(default=False)
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    updated_at = jmodels.jDateTimeField(auto_now=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='PENDING')
    delivery_date = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.pk is not None:
            old_instance = Order.objects.get(pk=self.pk)
            if old_instance.status != self.status:
                if self.status == "DELIVERED":
                    self.delivery_date = timezone.now()
                else:
                    self.delivery_date = None
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_at']),
        ]

        verbose_name = "سفارش"
        verbose_name_plural = "سفارشات"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_post_cost(self):
        total_weight = sum(item.get_weight() for item in self.items.all())

        if total_weight == 0:
            return 0
        elif total_weight < 1000:
            return 20000
        elif 1000 < total_weight < 2000:
            return 30000
        else:
            return 50000

    def get_final_cost(self):
        final_price = self.get_total_cost() + self.get_post_cost()
        return final_price

    def get_address(self):
        if hasattr(self, 'order') and self.order and self.order.address:
            order_address = self.order.address
            return (f"{order_address.first_name} {order_address.last_name} "
                    f"{order_address.address_line}")
        return "nothing"

    def get_first_name(self):
        return self.order.address.first_name if hasattr(self, 'order') and self.order and self.order.address else ""

    def get_last_name(self):
        return self.order.address.last_name if hasattr(self, 'order') and self.order and self.order.address else ""

    def get_phone_number(self):
        return self.order.address.phone_number if hasattr(self, 'order') and self.order and self.order.address else ""

    def __str__(self):
        return f'order: {self.id} - {self.buyer}'


class OrderAddress(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="order")
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name="order_address")


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_items')
    quantity = models.PositiveIntegerField(default=0)
    price = models.PositiveIntegerField(default=0)
    weight = models.PositiveIntegerField(default=0)

    def get_cost(self):
        return self.price * self.quantity

    def get_weight(self):
        return self.weight * self.quantity

    def __str__(self):
        return f"{self.id} - {self.product}"


class ReturnedProducts(models.Model):
    choice_status = [
        ('UNDER REVIEW', 'UNDER REVIEW'),
        ('CONFIRMATION', 'CONFIRMATION'),
        ('REJECTED', 'REJECTED'),
        ('COMPLETED', 'COMPLETED'),
        ('REFUNDED', 'REFUNDED'),
    ]
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    user = models.ForeignKey(ShopUser, on_delete=models.SET_NULL, null=True, blank=True)
    return_reason = models.TextField(default="Please explain your reason...")
    image = models.ImageField(upload_to='returned_products')
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=choice_status, default='UNDER REVIEW')

    class Meta:
        ordering = ['-request_date']
        indexes = [
            models.Index(fields=['-request_date']),
        ]

    def __str__(self):
        return f"{self.id} - {self.user}"













