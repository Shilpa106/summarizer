# Django imports
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator


# Inside App imports
from .managers import CustomUserManager
from Subscription.models import SubscriptionType


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True, db_index=True)
    username = models.CharField(_('username'), max_length=50, unique=True, db_index=True)
    phone_regex  = RegexValidator(regex=r'^\+?1?\d{9,15}$', message='Phone number must be entered in the format: "9999999999".')
    mobile       = models.CharField(max_length=15, validators=[phone_regex], blank=True, null=True)
    first_name   = models.CharField(max_length=100, blank=True, null=True)
    last_name   = models.CharField(max_length=100, blank=True, null=True)
    # is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)




    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()
    

    def __str__(self):
        return self.email



class Subscription(models.Model):
    user_id     = models.ForeignKey(User, on_delete=models.CASCADE)
    plan_id     = models.ForeignKey(SubscriptionType, on_delete=models.CASCADE)
    is_active   = models.BooleanField(default=True)
    activation_date  = models.DateTimeField(null=True, blank=True)
    end_date    = models.DateTimeField(null=True, blank=True)
    cretated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.plan_id.plan_name + " >> Validity: " + str(self.plan_id.plan_validity) + " months"