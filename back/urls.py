from django.urls import path
from api import views
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),

    # path('login/', views.login, name='login'),
    # path('user/', views.get_user, name='user'),

    # path('orders/', views.order_list, name='order-list'),
    # path('orders/<int:pk>/', views.order_detail, name='order-detail'),
    # path('shipping-couriers/', views.shipping_courier_list, name='shipping-courier-list'),
    # path('shipping-couriers/<int:pk>/', views.shipping_courier_detail, name='shipping-courier-detail'),
    # path('order-statuses/', views.order_status_list, name='order-status-list'),
    # path('order-statuses/<int:pk>/', views.order_status_detail, name='order-status-detail'),
    # path('sales/', views.sales_list, name='sales-list'),
    # path('sales/<int:pk>/', views.sales_detail, name='sales-detail'),
    # path('user-sales/create/', views.create_user_and_sales, name='user-sales-list'),
    
    # path('orders-data/', views.get_yearly_orders_data, name='orders-data'),

    
    # path('bags/', views.get_bags),
    # path('bags/<int:pk>/', views.get_bag),
    # path('bags/<int:pk>/delete/', views.delete_bag),
    # path('bags/create-update/', views.create_bag_with_order),
]
