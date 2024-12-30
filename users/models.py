from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from cloudinary.models import CloudinaryField

class Profile(models.Model):
    auth_user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="auth_user", primary_key=True
    )
    full_name = models.CharField(max_length=255, null=False, blank=False)
    is_crafter = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    craft_time_commited = models.IntegerField(validators=[MinValueValidator(1)], null=True, blank=True)
    craft_time_max = models.IntegerField(validators=[MinValueValidator(1)], null=True, blank=True)
    image = CloudinaryField('image', null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    deleted_on = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.full_name


class Newsletter(models.Model):
    profile = models.OneToOneField(
        Profile, on_delete=models.CASCADE, related_name="profile"
    )
    email = models.EmailField(unique=True)
    subscribed_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email