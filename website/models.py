from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.
class SiteMeta(models.Model):
    title = models.CharField(max_length=500)
    favicon = models.ImageField(upload_to='images')
    logo = models.ImageField(upload_to='images')
    logo_2 = models.ImageField(upload_to='images', blank=True, null=True)
    address = models.TextField(max_length=1000, null=True, blank=True)
    phone = models.CharField(max_length=13, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    footer_text = models.TextField(max_length=2000, null=True, blank=True)
    meta_title = models.CharField(max_length=500, blank=True, null=True)
    meta_description = models.TextField(max_length=2000, blank=True, null=True)
    meta_tags = models.TextField(max_length=1000, blank=True, null=True)

    def clean(self):
        if SiteMeta.objects.exists() and not self.pk:
            raise ValidationError("You cna only have one site meta settings.")

    def save(self, *args, **kwargs):
       return super(SiteMeta, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Site Setup'
        verbose_name_plural = 'Site Setup'

class Page(models.Model):
    page_name = models.CharField(max_length=100, null=True)
    title = models.CharField(max_length=500)
    description = models.TextField(max_length=2000, null=True, blank=True)
    image = models.ImageField(upload_to='images', blank=True, null=True)
    link = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.page_name

class PageSection(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField(max_length=2000, null=True, blank=True)
    image = models.ImageField(upload_to='images',blank=True,null=True)
    link = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.title

class InfoCard(models.Model):
    pagesection = models.ForeignKey(PageSection, on_delete=models.CASCADE, default=None, related_name='item_set')
    title = models.CharField(max_length=500,)
    subtitle = models.CharField(max_length=500, blank=True, null=True)
    description = models.TextField(max_length=2000, blank=True, null=True)
    image = models.ImageField(upload_to='images', blank=True, null=True)
    link = models.URLField(max_length=500, blank=True, null=True)
    icon = models.CharField(max_length=100, help_text="favicon, fontawesome etc icon class name")

    def __str__(self):
        return self.title
