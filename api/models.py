# from django.db import models
# from django.contrib.auth.models import User


# class ShippingCourier(models.Model):
#     name = models.CharField(max_length=255)

#     def __str__(self):
#         return self.name

# class OrderStatus(models.Model):
#     name = models.CharField(max_length=100)

#     def __str__(self):
#         return self.name

# class Sales(models.Model):
#     # Sales model linked to the built-in User model.
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='sales')
#     role = models.CharField(
#         max_length=50,
#         choices=[
#             ('seller', 'Seller'),
#             ('other', 'Other'),
#         ],
#         default='seller'
#     )

#     def __str__(self):
#         return self.user.get_full_name() or self.user.username


# class Bag(models.Model):
#     # basic details
#     name = models.CharField(max_length=255, null=True, blank=True)
#     date = models.DateField(null=True, blank=True)
#     # shipping details
#     weight = models.FloatField(null=True, blank=True, default=0)
#     shipping_company = models.ForeignKey(ShippingCourier, on_delete=models.SET_NULL, null=True, blank=True)
#     shipping_cost_in_egp = models.IntegerField(default=0, null=True, blank=True)
#     shipping_cost_in_sar = models.IntegerField(default=0, null=True, blank=True)
#     # financial details
#     price_in_egp = models.IntegerField(default=0, null=True, blank=True)
#     price_in_sar = models.IntegerField(default=0, null=True, blank=True)
#     profit_in_egp = models.IntegerField(default=0, null=True, blank=True)
#     profit_in_sar = models.IntegerField(default=0, null=True, blank=True)
#     discount_in_egp = models.IntegerField(default=0, null=True, blank=True)
#     discount_in_sar = models.IntegerField(default=0, null=True, blank=True)
#     xg = models.CharField(max_length=255, blank=True, null=True, default=None)

#     def __str__(self):
#         return self.name


# class Order(models.Model):
#     bag = models.ForeignKey(Bag, on_delete=models.CASCADE, related_name='orders')
#     # customer details
#     customer_name = models.CharField(max_length=255,null=True, blank=True)
#     customer_number = models.CharField(max_length=50,null=True, blank=True)
#     customer_note = models.CharField(blank=True, null=True)
#     how_many_pices = models.IntegerField(default=0, blank=True, null=True)
#     # pieces = models.JSONField(default=list)  # Store items as a list of dictionaries [{"code": "123", "price": 10}, {...}]
#     address = models.CharField(null=True, blank=True)
#     # order status
#     seller = models.ForeignKey(Sales, on_delete=models.SET_NULL, null=True, blank=True)
#     paid_in_egp = models.IntegerField(default=0,null=True, blank=True)
#     paid_in_sar = models.IntegerField(default=0,null=True, blank=True)
#     remaining_in_egp = models.IntegerField(default=0,null=True, blank=True)
#     remaining_in_sar = models.IntegerField(default=0,null=True, blank=True)
#     is_delivered = models.BooleanField(default=False,null=True, blank=True)
#     is_collected = models.BooleanField(default=False,null=True, blank=True)

#     def __str__(self):
#         return self.customer_name
    

# class Piece(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='pieces')
#     product = models.CharField(max_length=255, null=True, blank=True)
#     code = models.CharField(max_length=255, null=True, blank=True)
#     price_in_egp = models.IntegerField(default=0,null=True, blank=True)
#     price_in_sar = models.IntegerField(default=0,null=True, blank=True)

#     def __str__(self):
#         return f"{self.code}: {self.price}"


# class Image(models.Model):
#     piece = models.ForeignKey(Piece, on_delete=models.CASCADE, related_name='images')
#     image = models.ImageField(upload_to='images/')

#     def __str__(self):
#         return f"Image for {self.piece}"


# # class Order(models.Model):
# #     # Basic order information
# #     customer_name = models.CharField(max_length=255)
# #     customer_phone = models.CharField(max_length=50)
# #     customer_wp = models.CharField(max_length=50, blank=True, null=True)  # e.g. WhatsApp number

# #     # Foreign keys to other models
# #     order_status = models.ForeignKey(OrderStatus, on_delete=models.SET_NULL, null=True)
# #     shipping_courier = models.ForeignKey(ShippingCourier, on_delete=models.SET_NULL, null=True)
# #     sales = models.ForeignKey(Sales, on_delete=models.SET_NULL, null=True)

# #     # Financial and address details
# #     total_order_in_sar = models.IntegerField(default=0)
# #     total_order_in_eg = models.IntegerField(default=0)
# #     total_order_profit_in_sar = models.IntegerField(default=0)
# #     total_order_profit_in_eg = models.IntegerField(default=0)
# #     paid = models.IntegerField(default=0)
# #     remain = models.IntegerField(default=0)
# #     is_collected = models.BooleanField(default=False)
# #     address = models.CharField()
# #     shipping_cost = models.IntegerField(default=0)

# #     date = models.DateField(auto_now_add=True)

# #     def __str__(self):
# #         return f"Order {self.id} - {self.customer_name}"

from django.db import models

# Dummy models for ShippingCourier and Sales. Replace/expand as needed.
class ShippingCourier(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Sales(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Order(models.Model):
    # Basic details
    name = models.CharField(max_length=255, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    
    # Shipping details
    weight = models.FloatField(null=True, blank=True, default=0)
    shipping_company = models.ForeignKey(ShippingCourier, on_delete=models.SET_NULL, null=True, blank=True)
    shipping_cost_in_egp = models.IntegerField(default=0, null=True, blank=True)
    shipping_cost_in_sar = models.IntegerField(default=0, null=True, blank=True)
    
    # Financial details
    price_in_egp = models.IntegerField(default=0, null=True, blank=True)
    price_in_sar = models.IntegerField(default=0, null=True, blank=True)
    profit_in_egp = models.IntegerField(default=0, null=True, blank=True)
    profit_in_sar = models.IntegerField(default=0, null=True, blank=True)
    discount_in_egp = models.IntegerField(default=0, null=True, blank=True)
    discount_in_sar = models.IntegerField(default=0, null=True, blank=True)
    xg = models.CharField(max_length=255, blank=True, null=True, default=None)

    def update_totals(self):
        """
        This method loops over all related customers and their pieces to:
          - Sum the piece prices for EGP and SAR.
          - Update each customer's remaining amount (pieces total minus paid amounts).
          - Calculate the Order’s total price (pieces sum + shipping cost)
          - Subtract any discount to set the profit.
        Any None value is treated as 0.
        """
        total_pieces_egp = 0
        total_pieces_sar = 0

        # Loop through related customers (using the related_name from Customer)
        for customer in self.orders.all():
            customer_total_egp = 0
            customer_total_sar = 0
            # Sum prices of pieces for this customer
            for piece in customer.pieces.all():
                customer_total_egp += piece.price_in_egp or 0
                customer_total_sar += piece.price_in_sar or 0

            total_pieces_egp += customer_total_egp
            total_pieces_sar += customer_total_sar

            # Calculate remaining for customer (if paid amounts are entered)
            paid_egp = customer.paid_in_egp or 0
            paid_sar = customer.paid_in_sar or 0
            customer.remaining_in_egp = customer_total_egp - paid_egp
            customer.remaining_in_sar = customer_total_sar - paid_sar
            customer.save(update_fields=['remaining_in_egp', 'remaining_in_sar'])

        # Add shipping cost from the Order (treating None as 0)
        shipping_egp = self.shipping_cost_in_egp or 0
        shipping_sar = self.shipping_cost_in_sar or 0
        total_price_egp = total_pieces_egp + shipping_egp
        total_price_sar = total_pieces_sar + shipping_sar

        self.price_in_egp = total_price_egp
        self.price_in_sar = total_price_sar

        # Subtract discount to calculate profit
        discount_egp = self.discount_in_egp or 0
        discount_sar = self.discount_in_sar or 0
        self.profit_in_egp = total_price_egp - discount_egp
        self.profit_in_sar = total_price_sar - discount_sar

        # Save updated fields for Order. (Be mindful that this method may be called after inlines are saved.)
        self.save(update_fields=['price_in_egp', 'price_in_sar', 'profit_in_egp', 'profit_in_sar'])

    def __str__(self):
        return self.name or f"Order #{self.pk}"

class Customer(models.Model):
    # Note: related_name is 'orders' so that from an Order instance you can call order.orders.all()
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orders')
    
    # Customer details
    customer_name = models.CharField(max_length=255, null=True, blank=True)
    customer_number = models.CharField(max_length=50, null=True, blank=True)
    customer_note = models.CharField(max_length=1000, blank=True, null=True)
    how_many_pices = models.IntegerField(default=0, blank=True, null=True)
    address = models.CharField(max_length=1000, null=True, blank=True)
    
    # Order status
    seller = models.ForeignKey(Sales, on_delete=models.SET_NULL, null=True, blank=True)
    paid_in_egp = models.IntegerField(default=0, null=True, blank=True)
    paid_in_sar = models.IntegerField(default=0, null=True, blank=True)
    remaining_in_egp = models.IntegerField(default=0, null=True, blank=True)
    remaining_in_sar = models.IntegerField(default=0, null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.order.save()

    def __str__(self):
        return self.customer_name or f"Customer #{self.pk}"

class Piece(models.Model):
    # A Piece is linked to a Customer.
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='pieces')
    product_name = models.CharField(max_length=255)
    product_code = models.CharField(max_length=100)
    price_in_egp = models.IntegerField(default=0)
    price_in_sar = models.IntegerField(default=0)

    def __str__(self):
        return self.product_name

class PieceImage(models.Model):
    # Each PieceImage belongs to a Piece.
    piece = models.ForeignKey(Piece, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='piece_images/')

    def __str__(self):
        return f"Image for {self.piece.product_name}"
