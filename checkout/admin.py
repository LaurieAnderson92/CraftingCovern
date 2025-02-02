from django.contrib import admin
from .models import Order, OrderLineItem


class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('order_number','customer',
                       'date','delivery_cost',
                       'order_cost','grand_total',
                       'customization')
    
    ordering = ['-date']
    
    list_display = ('order_number',
                    'date','full_name',
                    'grand_total')


class OrderLineItemAdmin(admin.ModelAdmin):
    readonly_fields = ('order', 'product',
                       'lineitem_cost',)

ordering = ['order']

# Register your models here.
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderLineItem, OrderLineItemAdmin)
