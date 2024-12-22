import uuid

from django.db import models
from django.db.models import Sum
from django.conf import settings

from users.models import Profile
from products.models import Product
from django.contrib.auth.models import User

# Create your models here.

class Order(models.Model):

    order_number = models.CharField(max_length=32, null=False, editable=False)
    customer = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="customer", primary_key=True
    )
    product = models.ForeignKey(Product, null=True, blank=False, on_delete=models.SET_NULL)
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = models.CharField(max_length=40, null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)
    order_cost = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)

    def _generate_order_number(self):
        """
        Generate a random, unique order number using UUID
        """
        return uuid.uuid4().hex.upper()

    def update_order_cost(self):
        """
        Copy the amount the product was at the time of purchase
        """
        self.order_cost = self.product.cost
        tenpercernt = self.order_cost/10
        if tenpercernt > settings.MINIMUM_DELIVERY_CHARGE:
            self.delivery_cost = tenpercernt
        else:
            self.delivery_cost = settings.MINIMUM_DELIVERY_CHARG
        self.save()

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number