from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import OrderLineItem

@receiver(post_save, sender=OrderLineItem)
def update_on_save(sender, instance, created, **kwargs):
    """
    Update the totals of the order on line item creation or update
    """
    instance.order.update_order_cost()

@receiver(post_save, sender=OrderLineItem)
def update_on_delete(sender, instance, **kwargs):
    """
    Update the totals of the order on line item delete
    """
    instance.order.update_order_cost()