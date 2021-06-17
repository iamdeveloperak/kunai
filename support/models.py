from django.db import models

# Create your models here.
class Support(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=10)
    subject = models.CharField(max_length=200)
    message = models.TextField(max_length=2000)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'support'