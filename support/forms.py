from django import forms
from django.forms import ModelForm, Textarea, TextInput, EmailInput
from .models import Support
class SupportForm(forms.ModelForm):
    class Meta:
        model = Support
        fields = '__all__'
        widgets = {
            'name': TextInput(attrs={'placeholder':'Name'}),
            'email': EmailInput(attrs={'placeholder':'Email'}),
            'phone': TextInput(attrs={'placeholder':'Phone Number'}),
            'subject': TextInput(attrs={'placeholder':'Subject'}),
            'message': Textarea(attrs={'placeholder':'message'}),
        }