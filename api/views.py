from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
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
        orders = Order.objects.all().order_by('-bag__date')
    
        # order info
        sales_id = request.GET.get('sales_id')
        customer_name = request.GET.get('customer_name')
        customer_number = request.GET.get('customer_number')

        is_delivered = request.GET.get('is_delivered')
        is_collected = request.GET.get('is_collected')

        shipping_company = request.GET.get('shipping_company')

        date_from = request.GET.get('date_from')
        date_to = request.GET.get('date_to')

        if date_from:
            orders = orders.filter(bag__date__gte=date_from)
            
        if date_to:
            orders = orders.filter(bag__date__lte=date_to)

        if shipping_company:
            orders = orders.filter(bag__shipping_company__id=shipping_company)

        if customer_name:
            orders = orders.filter(customer_name__icontains=customer_name)
        if customer_number:
            orders = orders.filter(customer_number__icontains=customer_number)
        
        if str(is_delivered) == 'true':
            orders = orders.filter(is_delivered=True)
        if str(is_delivered) == 'false':
            orders = orders.filter(is_delivered=False)

        if str(is_collected) == 'true':
            orders = orders.filter(is_collected=True)
        if str(is_collected) == 'false':
            orders = orders.filter(is_collected=False)


        
        serializer = OrderSerializer(orders, many=True)
        
        data = {
            "orders": serializer.data,
        }


        all_orders_with_no_seller = []
        if sales_id:
            if str(sales_id) == 'no':
                orders = orders.filter(seller__id__isnull=True)
            else:
                all_orders_with_no_seller = orders # all
                orders = orders.filter(seller__id=sales_id) # seller

                serializer = OrderSerializer(orders, many=True)
                
                data = {
                    "orders": serializer.data,
                    "all_orders_with_no_seller": OrderSerializer(all_orders_with_no_seller, many=True).data
                }

        return Response(data)
    
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




from django.db import transaction

@api_view(['POST'])
def create_user_and_sales(request):
    user_data = request.data.get('user', {})
    sales_data = request.data.get('sales', {})

    with transaction.atomic():
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save()

            sales_data['user'] = user.id
            sales_serializer = SalesSerializer(data=sales_data)
            if sales_serializer.is_valid():
                sales_serializer.save()
                return Response({
                    'user': user_serializer.data,
                    'sales': sales_serializer.data
                }, status=status.HTTP_201_CREATED)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)




import calendar
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth

def filter_orders(request):
    orders = Order.objects.all()
    
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
        orders = orders.filter(seller__id=sales_id)
    
    return orders

@api_view(['GET'])
def get_yearly_orders_data(request):
    orders = filter_orders(request)

    year_param = request.GET.get('year')
    if not year_param:
        return Response({"error": "Year parameter is required"}, status=400)
    try:
        year = int(year_param)
    except ValueError:
        return Response({"error": "Invalid year parameter"}, status=400)

    # Filter orders by year on bag__date
    orders = orders.filter(bag__date__year=year)

    # Group by month and aggregate
    aggregated = orders.annotate(month=TruncMonth('bag__date')).values('month').annotate(
        total_orders_count=Count('id'),
        total_price=Sum('bag__price_in_egp', distinct=True),  # Sum unique bag prices
        total_profit=Sum('bag__profit_in_egp'),
        total_xg=Sum('bag__xg'),
    ).order_by('month')

    aggregated_dict = {}
    for entry in aggregated:
        if entry['month']:
            month_number = entry['month'].month
            aggregated_dict[month_number] = {
                "total_orders_count": entry['total_orders_count'] or 0,
                "total_price": entry['total_price'] or 0,
                "total_profit": entry['total_profit'] or 0,
                "total_xg": entry['total_xg'] or 0,
            }

    months_data = []
    for m in range(1, 13):
        month_name = calendar.month_name[m]
        data = aggregated_dict.get(m, {
            "total_orders_count": 0,
            "total_price": 0,
            "total_profit": 0,
            "total_xg": 0,
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



from django.db.models import Q, Sum, DecimalField
from django.db.models.functions import Coalesce
@api_view(['GET'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def get_bags(request):
    if request.method == 'GET':
        bgs = Bag.objects.all().order_by('-date')

        # date filters
        date_from = request.GET.get('date_from')
        date_to = request.GET.get('date_to')
        if date_from:
            bgs = bgs.filter(Q(date__gte=date_from) | Q(date__isnull=True))
        if date_to:
            bgs = bgs.filter(Q(date__lte=date_to) | Q(date__isnull=True))

        # closed
        is_closed = request.GET.get('is_closed')
        if str(is_closed).lower() == 'true':
            bgs = bgs.filter(is_closed=True)
        if str(is_closed).lower() == 'false':
            bgs = bgs.filter(is_closed=False)

        # shipping company filter
        shipping_company = request.GET.get('shipping_company')
        if shipping_company:
            bgs = bgs.filter(shipping_company__id=shipping_company)


        
        # Seller profit calculations (no filtering of bags)
        seller_id = request.GET.get('seller')
        temp_bags = []
        bags_profit_egp = 0
        orders_profit_egp = 0
        
        if seller_id:
            # bags_profit_egp
            for i in bgs:
                if i in temp_bags:
                    continue
                else:
                    temp_bags.append(i)
                    bags_profit_egp += i.profit_in_egp

            # orders_profit_egp
            temp_orders = []
            temp_order_bag = []
            for i in temp_bags:
                bag_orders = Order.objects.filter(bag=i)
                for order in bag_orders:
                    if order:
                        if order.pk in temp_orders:
                            continue
                        else:
                            if str(seller_id) == str(getattr(order.seller, 'pk', "")):
                                if order.bag.pk in temp_order_bag:
                                    continue
                                else:
                                    temp_orders.append(order.pk)
                                    temp_order_bag.append(order.bag.pk)
                                    orders_profit_egp += order.bag.profit_in_egp

        serializer = BagSerializer(bgs, many=True)

        data = {
            "bags": serializer.data,
            "bags_profit_egp": float(bags_profit_egp) if bags_profit_egp else 0.0,
            "orders_profit_egp": float(orders_profit_egp) if orders_profit_egp else 0.0,
        }
        return Response(data)
    

@api_view(['GET'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def get_bag(request, pk):
    if request.method == 'GET':
        bag = get_object_or_404(Bag, pk=pk)
        serializer = OneBagSerializer(bag)
        return Response(serializer.data)


@api_view(['DELETE'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def delete_bag(request, pk):
    if request.method == 'DELETE':
        bag = get_object_or_404(Bag, pk=pk)
        bag.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# create order with Bag
@api_view(['POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def create_bag_with_order(request):
    if request.method == 'POST':
        bag_data = request.data.get("bag")
        orders_data = request.data.get("orders", [])

        print(orders_data)

        date_data = bag_data.get("date")
        if str(date_data) == '':
            bag_data["date"] = None

        if not bag_data:
            return Response({"error": "Bag data is required."}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            # Process the shipping_company field
            shipping_company_input = bag_data.get("shipping_company")
            if shipping_company_input:
                try:
                    shipping_courier = ShippingCourier.objects.get(name=shipping_company_input)
                except ShippingCourier.DoesNotExist:
                    shipping_courier = ShippingCourier.objects.create(name=shipping_company_input)
                # Replace text with the ShippingCourier's id
                bag_data["shipping_company"] = shipping_courier
            else:
                bag_data["shipping_company"] = None

            bag_id = bag_data.get("id")
            if bag_id:
                try:
                    bag = Bag.objects.get(id=bag_id)
                    # Update bag fields (except id)
                    for key, value in bag_data.items():
                        if key != "id":
                            setattr(bag, key, value)
                    bag.save()
                except Bag.DoesNotExist:
                    bag = Bag.objects.create(**bag_data)
            else:
                bag = Bag.objects.create(**bag_data)

            # Process orders
            existing_orders = Order.objects.filter(bag=bag)
            provided_order_ids = set()

            for order_item in orders_data:
                order_id = order_item.get("id")
                seller_name = order_item.get("seller")

                seller = None
                if seller_name:
                    try:
                        seller = Sales.objects.get(user__username=seller_name)
                    except Sales.DoesNotExist:
                        pass
                order_item["seller"] = seller

                # bag_id = order_item.get("bag")
                # bag = None
                # if bag_id:
                #     try:
                #         bag = Bag.objects.get(id=bag_id)
                #     except Bag.DoesNotExist:
                #         pass
                # order_item["bag"] = bag

                if order_id:
                    provided_order_ids.add(order_id)
                    try:
                        # Update the order if it exists and is related to this bag
                        order = Order.objects.get(id=order_id, bag=bag)
                        for key, value in order_item.items():
                            if key != "id":
                                if key == "bag":
                                    value = bag
                                setattr(order, key, value)
                        order.save()
                    except Order.DoesNotExist:
                        # If provided id does not exist for this bag, create a new order
                        order_item.pop("id", None)
                        order = Order.objects.create(bag=bag, **order_item)
                        provided_order_ids.add(order.id)
                else:
                    # Create a new order if no id is provided
                    order = Order.objects.create(bag=bag, **order_item)
                    provided_order_ids.add(order.id)

            # Delete orders that existed before but are not present in the new data
            orders_to_delete = existing_orders.exclude(id__in=provided_order_ids)
            orders_to_delete.delete()

        return Response(BagSerializer(bag).data, status=status.HTTP_201_CREATED)
        # return Response({"bag_id": bag.id, "order_ids": list(provided_order_ids)}, status=status.HTTP_201_CREATED)



from datetime import datetime

@api_view(['GET'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def get_bag_for_graph(request):
    # Get the dates range from the request
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    # Make these dates range as months names
    from_month = datetime.strptime(date_from, '%Y-%m-%d').strftime('%B')
    to_month = datetime.strptime(date_to, '%Y-%m-%d').strftime('%B')

    # Get all bags in this range
    bags = Bag.objects.filter(date__range=(date_from, date_to))

    # Collect every bag that in the same month and calculate these fields and add them under this month
    data = {}
    for bag in bags:
        month = bag.date.strftime('%B')
        data.setdefault(month, {})
        data[month].setdefault('price_in_egp', 0)
        data[month].setdefault('profit_in_egp', 0)

        data[month]['price_in_egp'] += bag.price_in_egp
        data[month]['profit_in_egp'] += bag.profit_in_egp

    # Return the data
    return Response(data, status=status.HTTP_200_OK)

