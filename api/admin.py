# from django.contrib import admin
# import nested_admin
# from .models import *

# from rangefilter.filters import (
#     DateRangeQuickSelectListFilterBuilder,
# )


# class PieceImageInline(nested_admin.NestedTabularInline):
#     model = PieceImage
#     extra = 0


# class PieceInline(nested_admin.NestedTabularInline):
#     model = Piece
#     extra = 0
#     inlines = [PieceImageInline]


# class CustomerInline(nested_admin.NestedStackedInline):
#     model = Customer
#     extra = 0
#     inlines = [PieceInline]
#     fields = (
#         'order',
#         ('customer_name', 'customer_number'),
#         'customer_note',
#         'how_many_pices',
#         'address',
#         'seller',
#         ('paid_in_egp', 'paid_in_sar'),
#         ('remaining_in_egp', 'remaining_in_sar'),
#     )



# class OrderAdmin(nested_admin.NestedModelAdmin):
#     inlines = [CustomerInline]
#     list_display = ('name', 'date', 'weight', 'shipping_company', 'get_shipping_cost', 'get_price', 'get_discount', 'get_profit', 'xg')
#     fields = (
#         'name',
#         'date',
#         'weight',
#         'shipping_company',
#         ('shipping_cost_in_egp',
#         'shipping_cost_in_sar'),
#         ('price_in_egp',
#         'profit_in_sar'),
#         ('discount_in_egp',
#         'price_in_sar'),
#         ('profit_in_egp',
#         'discount_in_sar'),
#         'xg',
#     )

#     list_filter = (
#         ("date", DateRangeQuickSelectListFilterBuilder()),  # Range + QuickSelect Filter
#         'shipping_company',
#     )

#     search_fields = ['name', 'orders__customer_name', 'orders__customer_number']

#     def get_shipping_cost(self, obj):
#         return f"{obj.shipping_cost_in_egp} EGP / {obj.shipping_cost_in_sar} SAR"
#     get_shipping_cost.short_description = 'Shipping Cost'

#     def get_price(self, obj):
#         return f"{obj.price_in_egp} EGP / {obj.price_in_sar} SAR"
#     get_price.short_description = 'Price'

#     def get_discount(self, obj):
#         return f"{obj.discount_in_egp} EGP / {obj.discount_in_sar} SAR"
#     get_discount.short_description = 'Discount'

#     def get_profit(self, obj):
#         return f"{obj.profit_in_egp} EGP / {obj.profit_in_sar} SAR"
#     get_profit.short_description = 'Profit'


#     def save_related(self, request, form, formsets, change):
#         # Save all related inlines first...
#         super().save_related(request, form, formsets, change)
#         # Then update totals on the Order instance
#         order = form.instance
#         order.update_totals()

# admin.site.register(Order, OrderAdmin)


# class CustomerAdmin(nested_admin.NestedModelAdmin):
#     list_display = ('order', 'customer_name', 'get_how_many_pices', 'get_paid', 'get_remaining', 'seller', 'order__date')
#     fields = (
#         'order',
#         ('customer_name', 'customer_number'),
#         'customer_note',
#         'how_many_pices',
#         'address',
#         'seller',
#         ('paid_in_egp', 'paid_in_sar'),
#         ('remaining_in_egp', 'remaining_in_sar'),
#     )
#     search_fields = ['customer_name', 'customer_number', 'order__name']

#     list_filter = (
#         ("order__date", DateRangeQuickSelectListFilterBuilder()),  # Range + QuickSelect Filter
#     )

#     def get_how_many_pices(self, obj):
#         if obj.how_many_pices == 0 or obj.how_many_pices is None:
#             return obj.pieces.count()
#         return obj.how_many_pices
#     get_how_many_pices.short_description = 'How Many Pices'

#     def get_paid(self, obj):
#         return f"{obj.paid_in_egp} EGP / {obj.paid_in_sar} SAR"
#     get_paid.short_description = 'Paid'

#     def get_remaining(self, obj):
#         return f"{obj.remaining_in_egp} EGP / {obj.remaining_in_sar} SAR"
#     get_remaining.short_description = 'Remaining'


# admin.site.register(Customer, CustomerAdmin)
# admin.site.register(Sales)
# admin.site.register(ShippingCourier)


from django.contrib import admin

from .models import *

from django.contrib import admin

class ImageInline(admin.TabularInline):
    model = Image
    extra = 0


class PieceInline(admin.TabularInline):
    model = Piece
    extra = 0
    inlines = [ImageInline]  # This will not work directly without the trick below

    def get_inline_instances(self, request, obj=None):
        # Enable ImageInline inside PieceInline
        inlines = super().get_inline_instances(request, obj)
        if obj:
            return inlines + [ImageInline(self.model, self.admin_site)]
        return inlines


class OrderInline(admin.TabularInline):
    model = Order
    extra = 0
    show_change_link = True  # This makes the Order editable with a + button
    inlines = [PieceInline]

    def get_inline_instances(self, request, obj=None):
        # Enable PieceInline inside OrderInline
        inlines = super().get_inline_instances(request, obj)
        if obj:
            return inlines + [PieceInline(self.model, self.admin_site)]
        return inlines


class BagAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'weight', 'shipping_company', 'display_shipping_cost', 'display_profit')
    inlines = [OrderInline]

    def display_shipping_cost(self, obj):
        return f"{obj.shipping_cost_in_egp} EGP / {obj.shipping_cost_in_sar} SAR"
    display_shipping_cost.short_description = 'Shipping Cost'

    def display_profit(self, obj):
        return f"{obj.profit_in_egp} EGP / {obj.profit_in_sar} SAR"
    display_profit.short_description = 'Profit'


admin.site.register(Bag, BagAdmin)
admin.site.register(Order)
admin.site.register(Piece)
admin.site.register(Image)

admin.site.register(ShippingCourier)
admin.site.register(Sales)
# admin.site.register(OrderStatus)

