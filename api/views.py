from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Order, ShippingCourier, OrderStatus, Sales
from .serializers import OrderSerializer, ShippingCourierSerializer, OrderStatusSerializer, SalesSerializer, UserSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token



@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response("missing user", status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(user)
    return Response({'token': token.key, 'user': serializer.data})


@api_view(['GET'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def get_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

# ----- Order Views -----
@api_view(['GET', 'POST'])
def order_list(request):
    if request.method == 'GET':
        orders = Order.objects.all().order_by('-id')
        # date
        date_from = request.GET.get('date_from')
        date_to = request.GET.get('date_to')
        # order info
        sales_id = request.GET.get('sales_id')
        customer_name = request.GET.get('customer_name')
        customer_phone = request.GET.get('customer_phone')
        customer_wp = request.GET.get('customer_wp')
        # shipping
        order_status = request.GET.get('order_status')
        shipping_courier = request.GET.get('shipping_courier')
        is_collected = request.GET.get('is_collected')

        if date_from:
            orders = orders.filter(date__gte=date_from)
        if date_to:
            orders = orders.filter(date__lte=date_to)
        if sales_id:
            orders = orders.filter(sales__id=sales_id)
        if customer_name:
            orders = orders.filter(customer_name__icontains=customer_name)
        if customer_phone:
            orders = orders.filter(customer_phone__icontains=customer_phone)
        if customer_wp:
            orders = orders.filter(customer_wp__icontains=customer_wp)
        if order_status:
            orders = orders.filter(order_status__name=order_status)
        if shipping_courier:
            orders = orders.filter(shipping_courier__id=shipping_courier)
        if str(is_collected) == 'true':
            orders = orders.filter(is_collected=True)

        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def order_detail(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = OrderSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# ----- Shipping Courier Views -----
@api_view(['GET', 'POST'])
def shipping_courier_list(request):
    if request.method == 'GET':
        couriers = ShippingCourier.objects.all()
        serializer = ShippingCourierSerializer(couriers, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ShippingCourierSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def shipping_courier_detail(request, pk):
    try:
        courier = ShippingCourier.objects.get(pk=pk)
    except ShippingCourier.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = ShippingCourierSerializer(courier)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = ShippingCourierSerializer(courier, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        courier.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# ----- Order Status Views -----
@api_view(['GET', 'POST'])
def order_status_list(request):
    if request.method == 'GET':
        statuses = OrderStatus.objects.all()
        serializer = OrderStatusSerializer(statuses, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = OrderStatusSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def order_status_detail(request, pk):
    try:
        status_obj = OrderStatus.objects.get(pk=pk)
    except OrderStatus.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = OrderStatusSerializer(status_obj)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = OrderStatusSerializer(status_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        status_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# ----- Sales Views -----
@api_view(['GET', 'POST'])
def sales_list(request):
    if request.method == 'GET':
        sales = Sales.objects.all()
        serializer = SalesSerializer(sales, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        data = request.data.copy()
        serializer = SalesSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def sales_detail(request, pk):
    try:
        sales_obj = Sales.objects.get(pk=pk)
    except Sales.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = SalesSerializer(sales_obj)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = SalesSerializer(sales_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        sales_obj.user.delete()
        sales_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




@api_view(['POST'])
def create_user_and_sales(request):
    """
    Create a new user and associated sales record.
    """
    user_data = request.data.get('user', {})
    sales_data = request.data.get('sales', {})
    
    user_serializer = UserSerializer(data=user_data)
    if user_serializer.is_valid():
        user = user_serializer.save()
        
        # Create Sales entry linked to the user
        sales_data['user'] = user.id  # Associate user with sales
        sales_serializer = SalesSerializer(data=sales_data)
        
        if sales_serializer.is_valid():
            sales_serializer.save()
            return Response({
                'user': user_serializer.data,
                'sales': sales_serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            user.delete()  # Rollback user creation if sales fails
            return Response(sales_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)




import calendar
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth

def filter_orders(request):
    orders = Order.objects.all()
    
    # Date filters
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    if date_from:
        orders = orders.filter(date__gte=date_from)
    if date_to:
        orders = orders.filter(date__lte=date_to)
    
    # Other filters
    sales_id = request.GET.get('sales_id')
    customer_number = request.GET.get('customer_number')
    order_status = request.GET.get('order_status')
    is_collected = request.GET.get('is_collected')

    if customer_number:
        orders = orders.filter(customer_phone__icontains=customer_number)
    if order_status:
        orders = orders.filter(order_status__id=order_status)
    if str(is_collected).lower() == 'true':
        orders = orders.filter(is_collected=True)
    if sales_id:
        orders = orders.filter(sales__id=sales_id)
    
    return orders

@api_view(['GET'])
def get_yearly_orders_data(request):
    """
    Expected GET parameters:
      - year (e.g. ?year=2025)
      - (optional) other filters as in filter_orders
    """
    orders = filter_orders(request)
    
    year_param = request.GET.get('year')
    if not year_param:
        return Response({"error": "Year parameter is required"}, status=400)
    try:
        year = int(year_param)
    except ValueError:
        return Response({"error": "Invalid year parameter"}, status=400)
    
    # Filter orders for the selected year
    orders = orders.filter(date__year=year)
    
    # Group orders by month and aggregate
    aggregated = orders.annotate(month=TruncMonth('date')).values('month').annotate(
        total_orders_sar=Sum('total_order_in_sar'),
        total_orders_egp=Sum('total_order_in_eg'),
        total_profit_sar=Sum('total_order_profit_in_sar'),
        total_profit_egp=Sum('total_order_profit_in_eg'),
        total_shipping_cost=Sum('shipping_cost'),
        total_orders_count=Count('id')
    ).order_by('month')
    
    # Create a dictionary keyed by month number (1-12)
    aggregated_dict = {}
    for entry in aggregated:
        if entry['month']:
            month_number = entry['month'].month
            aggregated_dict[month_number] = {
                "total_orders_sar": entry['total_orders_sar'] or 0,
                "total_orders_egp": entry['total_orders_egp'] or 0,
                "total_profit_sar": entry['total_profit_sar'] or 0,
                "total_profit_egp": entry['total_profit_egp'] or 0,
                "total_shipping_cost": entry['total_shipping_cost'] or 0,
                "total_orders_count": entry['total_orders_count'] or 0,
            }
    
    # Build the result for all months (1 to 12)
    months_data = []
    for m in range(1, 13):
        month_name = calendar.month_name[m]
        data = aggregated_dict.get(m, {
            "total_orders_sar": 0,
            "total_orders_egp": 0,
            "total_profit_sar": 0,
            "total_profit_egp": 0,
            "total_shipping_cost": 0,
            "total_orders_count": 0,
        })
        months_data.append({
            "month_number": m,
            "month_name": month_name,
            **data
        })
    
    return Response({
        "year": year,
        "months": months_data
    })


