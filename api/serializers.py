from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Order, ShippingCourier, OrderStatus, Sales
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    role = serializers.ReadOnlyField(source='sales.role')
    class Meta():
        model = User 
        fields = '__all__'


class ShippingCourierSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingCourier
        fields = '__all__'

class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatus
        fields = '__all__'

class SalesSerializer(serializers.ModelSerializer):
    user_username = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Sales
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    order_status_name = serializers.ReadOnlyField(source='order_status.name')
    class Meta:
        model = Order
        fields = '__all__'
