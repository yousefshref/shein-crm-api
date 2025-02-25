from django.contrib import admin

from .models import Order, ShippingCourier, OrderStatus, Sales

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'customer_phone', 'shipping_courier', 'order_status', 'sales', 'total_order_in_sar', 'total_order_in_eg', 'paid', 'remain', 'is_collected', 'address', 'shipping_cost', 'date')
    
admin.site.register(Order, OrderAdmin)
admin.site.register(ShippingCourier)
admin.site.register(OrderStatus)
admin.site.register(Sales)
