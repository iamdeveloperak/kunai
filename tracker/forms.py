from django import forms
from .models import Product
from django.forms import URLInput

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('link',)
        widgets = {
            'link' : forms.URLInput(attrs={'placeholder':'Amazon Product Link. https://www.amazon.com/'})
        }