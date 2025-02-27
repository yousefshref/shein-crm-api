from django.db import models
from django.contrib.auth.models import User


class ShippingCourier(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class OrderStatus(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Sales(models.Model):
    # Sales model linked to the built-in User model.
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='sales')
    role = models.CharField(
        max_length=50,
        choices=[
            ('seller', 'Seller'),
            ('other', 'Other'),
        ],
        default='seller'
    )

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class Bag(models.Model):
    # basic details
    name = models.CharField(max_length=255)
    date = models.DateField(null=True, blank=True)
    # shipping details
    weight = models.FloatField(null=True, blank=True, default=0)
    shipping_company = models.ForeignKey(ShippingCourier, on_delete=models.SET_NULL, null=True)
    shipping_cost_in_egp = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipping_cost_in_sar = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # financial details
    price_in_egp = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price_in_sar = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    profit_in_egp = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    profit_in_sar = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_in_egp = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_in_sar = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    xg = models.CharField(max_length=255, blank=True, null=True, default=None)

    def __str__(self):
        return self.name


class Order(models.Model):
    bag = models.ForeignKey(Bag, on_delete=models.CASCADE, related_name='orders')
    # customer details
    customer_name = models.CharField(max_length=255)
    customer_number = models.CharField(max_length=50)
    customer_note = models.TextField(blank=True, null=True)
    pieces = models.JSONField(default=list)  # Store items as a list of dictionaries [{"code": "123", "price": 10}, {...}]
    address = models.TextField()
    # order status
    seller = models.ForeignKey(Sales, on_delete=models.SET_NULL, null=True)
    paid_in_egp = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    paid_in_sar = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    remaining_in_egp = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    remaining_in_sar = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_delivered = models.BooleanField(default=False)
    is_collected = models.BooleanField(default=False)

    def __str__(self):
        return self.customer_name



# class Order(models.Model):
#     # Basic order information
#     customer_name = models.CharField(max_length=255)
#     customer_phone = models.CharField(max_length=50)
#     customer_wp = models.CharField(max_length=50, blank=True, null=True)  # e.g. WhatsApp number

#     # Foreign keys to other models
#     order_status = models.ForeignKey(OrderStatus, on_delete=models.SET_NULL, null=True)
#     shipping_courier = models.ForeignKey(ShippingCourier, on_delete=models.SET_NULL, null=True)
#     sales = models.ForeignKey(Sales, on_delete=models.SET_NULL, null=True)

#     # Financial and address details
#     total_order_in_sar = models.IntegerField(default=0)
#     total_order_in_eg = models.IntegerField(default=0)
#     total_order_profit_in_sar = models.IntegerField(default=0)
#     total_order_profit_in_eg = models.IntegerField(default=0)
#     paid = models.IntegerField(default=0)
#     remain = models.IntegerField(default=0)
#     is_collected = models.BooleanField(default=False)
#     address = models.TextField()
#     shipping_cost = models.IntegerField(default=0)

#     date = models.DateField(auto_now_add=True)

#     def __str__(self):
#         return f"Order {self.id} - {self.customer_name}"
