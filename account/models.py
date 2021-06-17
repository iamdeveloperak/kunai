from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from datetime import datetime
# Create your models here.

class CustomUser(AbstractUser):
    phone_number = models.CharField(_('phone number'), max_length=13, unique=True, error_messages={'unique': _("A user with that phone number already exists."),},)
    email = models.EmailField(_('email address'), unique=True, error_messages={'unique': _("A user with that email already exists."),},)
    is_premium = models.BooleanField(_('Premium'), default=False, help_text=_('Designates whether this user should be treated as premium. '),)
    REQUIRED_FIELDS = ['email','phone_number']
    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        db_table = 'user'

    @property
    def is_premium_user(self):
        """
        this property tells if a user is premium or free.
        """
        from membership.models import UserMembership, Subscription, Membership
        from tracker.models import Product
        try:
            um = UserMembership.objects.get(user = self)
            subscription = Subscription.objects.filter(user_membership = um)
            if subscription.count() > 0:
                if datetime.now().date() > subscription[0].expires_in:
                    membership = Membership.objects.get(slug='free')
                    um.membership = membership
                    um.payment_status = 3
                    um.save()
                    subscription[0].delete()
                    products = Product.objects.filter(user=self)
                    if products.count() > 3:
                        for p in enumerate(products):
                            if p[0] >= 3:
                                p[1].delete()
                    self.is_premium = False
                    self.save()
            else:
                # um.order_id = None
                # um.datetime_of_payment = None
                # um.razorpay_order_id = None
                # um.razorpay_payment_id = None
                # um.razorpay_signature = None
                um.save()
                # um.delete()
                # membership = Membership.objects.get(slug='free')
                # usermembership = UserMembership.objects.get_or_create(user=self, membership=membership)
                products = Product.objects.filter(user=self)
                if products.count() > 3:
                    for p in enumerate(products):
                        if p[0] >= 3:
                            p[1].delete()
                self.is_premium = False
                self.save()

        except Exception as e:
            print('kunai.account.models except block', e)

        return self.is_premium


