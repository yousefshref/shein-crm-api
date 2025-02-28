from django.contrib import admin

from .models import *

admin.site.register(Order)
admin.site.register(ShippingCourier)
admin.site.register(OrderStatus)
admin.site.register(Sales)
admin.site.register(Bag)
