from decimal import Decimal
from django.conf import settings


def cart_contents(request):

    cart_items = []
    total = 0
    products_count = 0

    tenpercernt = total/10
    delivery_cost = 0

    if tenpercernt > settings.MINIMUM_DELIVERY_CHARGE:
        delivery_cost = Decimal(tenpercernt)
    else:
        delivery_cost = settings.MINIMUM_DELIVERY_CHARGE

    grand_total = total + delivery_cost

    context = {
        "cart_items": cart_items,
        "total": total,
        "products_count": products_count, 
        "delivery_cost": delivery_cost,
        "grand_total": grand_total,
    }

    print("Context processor Loaded")

    return context