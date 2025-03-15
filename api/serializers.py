from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Order, ShippingCourier, OrderStatus, Sales, Bag
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    role = serializers.ReadOnlyField(source='sales.role')
    
    class Meta:
        model = User 
        fields = '__all__'
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user





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
    seller_id = serializers.ReadOnlyField(source='seller.id')
    seller_name = serializers.ReadOnlyField(source='seller.user.username')
    seller = serializers.ReadOnlyField(source='seller.user.username')
    bag_name = serializers.ReadOnlyField(source='bag.name')
    date = serializers.ReadOnlyField(source='bag.date')
    discount_in_egp = serializers.ReadOnlyField(source='bag.discount_in_egp')
    
    class Meta:
        model = Order
        fields = '__all__'


class BagSerializer(serializers.ModelSerializer):
    shipping_company_name = serializers.ReadOnlyField(source='shipping_company.name')
    total_paid_in_egp = serializers.SerializerMethodField(read_only=True)
    total_pieces = serializers.SerializerMethodField(read_only=True)

    def get_total_paid_in_egp(self, obj):
        orders = obj.orders.all()
        total = 0
        for order in orders:
            total += order.paid_in_egp
        return total

    def get_total_pieces(self, obj):
        orders = obj.orders.all()
        total = 0
        for order in orders:
            if order.how_many_pices > 0:
                total += order.how_many_pices
            else:
                total += len(order.pieces)
        return total
    
    class Meta:
        model = Bag
        fields = '__all__'


class OneBagSerializer(serializers.ModelSerializer):
    shipping_company_name = serializers.ReadOnlyField(source='shipping_company.name')
    orders_details = OrderSerializer(many=True, read_only=True, source='orders')
    class Meta:
        model = Bag
        fields = '__all__'
