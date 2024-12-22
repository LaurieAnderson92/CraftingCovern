from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from cloudinary.models import CloudinaryField

class User(models.Model):
    auth_user = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name="auth_user"
    )
    first_name = models.CharField(max_length=254)
    last_name = models.CharField(max_length=254)
    is_crafter = models.BooleanField()
    is_admin = models.BooleanField()
    craft_time_commited = models.IntegerField(validators=[MinValueValidator(1)])
    craft_time_max = models.IntegerField(validators=[MinValueValidator(1)])
    image = CloudinaryField('image',)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    deleted_on = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name
