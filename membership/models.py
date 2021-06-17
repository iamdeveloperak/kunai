from django.db import models
from django.db.models.deletion import CASCADE
from django.dispatch import receiver
from datetime import datetime as dt
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from django.db.models.signals import post_save, pre_save
from django.utils import timezone
from account.models import CustomUser
from kunai import settings
# Create your models here.


class Membership(models.Model):
    MEMBERSHIP_CHOICE = (
        ('free', 'Free'),
        ('Premium', 'Premium'),
    )
    PERIOD_DURATION = (
        ('month', 'Month'),
        ('year', 'Year'),
        ('lifetime', 'Life Time'),
    )
    slug = models.SlugField(null=True, blank=True)
    membership_type = models.CharField(choices=MEMBERSHIP_CHOICE, default='free', max_length=30)
    duration = models.IntegerField(default=1)
    duration_period = models.CharField(choices=PERIOD_DURATION, max_length=100, default='month')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.membership_type + ' ' + self.duration_period

class PayHistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None)
    payment_for = models.ForeignKey(Membership, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class UserMembership(models.Model):
    payment_status_choices = (
        (1, 'SUCCESS'),
        (2, 'FAILURE' ),
        (3, 'PENDING'),
    )
    user = models.OneToOneField(CustomUser, related_name='user_membership', on_delete=models.CASCADE)
    membership = models.ForeignKey(Membership, related_name='user_membership', on_delete=models.SET_NULL, null=True)
    payment_status = models.IntegerField(choices = payment_status_choices, default=3)
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True, default=None) 
    datetime_of_payment = models.DateTimeField(default=timezone.now, null=True)
    razorpay_order_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.user.email

    def save(self, *args, **kwargs):
        if self.order_id is None and self.datetime_of_payment and self.id:
            self.order_id = self.datetime_of_payment.strftime('MO_%Y%m%d%H%M%S%f') + str(self.id)
        return super().save(*args, **kwargs)

class Subscription(models.Model):
    user_membership = models.ForeignKey(UserMembership, related_name='subscription', on_delete=models.CASCADE)
    expires_in = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.user_membership.user.username


# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_membership(sender, instance, created, *args, **kwargs):
    if created:
        membership = Membership.objects.get(slug='free')
        usermembership = UserMembership.objects.get_or_create(user=instance, membership=membership)

post_save.connect(create_user_membership, sender=settings.AUTH_USER_MODEL)