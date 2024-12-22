from django.contrib import admin
from .models import Order

class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('order_number','customer','product','date','delivery_cost','order_cost','grand_total')

    ordering = ['-date']

    list_display = ('order_number','date','full_name','grand_total')


# Register your models here.
admin.site.register(Order, OrderAdmin)
