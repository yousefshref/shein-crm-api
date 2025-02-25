import random
from datetime import date, timedelta

from django.core.management.base import BaseCommand
from faker import Faker

from api.models import Order, OrderStatus, ShippingCourier, Sales  # adjust the import path as needed

class Command(BaseCommand):
    help = 'Create random orders with dates spanning a given range'

    def add_arguments(self, parser):
        parser.add_argument(
            '--start_date',
            type=str,
            default='2023-01-01',
            help='Start date in YYYY-MM-DD format (default: 2023-01-01)'
        )
        parser.add_argument(
            '--end_date',
            type=str,
            default='2023-12-31',
            help='End date in YYYY-MM-DD format (default: 2023-12-31)'
        )
        parser.add_argument(
            '--num_orders',
            type=int,
            default=1,
            help='Number of orders to create for each day (default: 1)'
        )

    def handle(self, *args, **options):
        fake = Faker()
        start_date = date.fromisoformat(options['start_date'])
        end_date = date.fromisoformat(options['end_date'])
        num_orders = options['num_orders']

        # Get available foreign key objects, if any
        order_statuses = list(OrderStatus.objects.all())
        shipping_couriers = list(ShippingCourier.objects.all())
        sales_people = list(Sales.objects.all())

        current_date = start_date
        total_orders = 0

        while current_date <= end_date:
            for _ in range(num_orders):
                Order.objects.create(
                    customer_name=fake.name(),
                    customer_phone=fake.phone_number(),
                    customer_wp=fake.phone_number(),
                    order_status=random.choice(order_statuses) if order_statuses else None,
                    shipping_courier=random.choice(shipping_couriers) if shipping_couriers else None,
                    sales=random.choice(sales_people) if sales_people else None,
                    total_order_in_sar=random.randint(50, 1000),
                    total_order_in_eg=random.randint(50, 1000),
                    total_order_profit_in_sar=random.randint(10, 500),
                    total_order_profit_in_eg=random.randint(10, 500),
                    paid=random.randint(0, 1000),
                    remain=random.randint(0, 1000),
                    is_collected=random.choice([True, False]),
                    address=fake.address(),
                    shipping_cost=random.randint(0, 100),
                    date=current_date
                )
                total_orders += 1
            self.stdout.write(self.style.SUCCESS(f"Created {num_orders} orders for {current_date}"))
            current_date += timedelta(days=1)

        self.stdout.write(self.style.SUCCESS(f"Successfully created {total_orders} orders."))
