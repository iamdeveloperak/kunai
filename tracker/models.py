from django.db import models
from account.models import CustomUser
from django.conf import settings
# Create your models here.
class Product(models.Model):
    id = models.BigAutoField(primary_key=True)
    link = models.URLField(max_length=500, null=False, blank=False)
    title = models.CharField(max_length=500, null=False, blank=False)
    availability = models.CharField(max_length=30)
    image = models.ImageField(upload_to='products')
    price = models.PositiveIntegerField()
    deal_price = models.PositiveIntegerField(default=0)
    changed_price = models.PositiveIntegerField(default=0)
    redused_price = models.PositiveIntegerField(default=0)
    on_sale = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'product'
        verbose_name = 'product'
        verbose_name_plural = 'products'