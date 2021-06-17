from django import forms
from django.forms import TextInput, EmailInput, PasswordInput
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordChangeForm
from .models import CustomUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.views import PasswordContextMixin
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('first_name','last_name','username','email','phone_number','password1','password2')
        widgets = {
            'first_name': TextInput(attrs={'placeholder':'First Name'}),
            'last_name': TextInput(attrs={'placeholder':'Last Name'}),
            'username': TextInput(attrs={'placeholder':'Username'}),
            'email': EmailInput(attrs={'placeholder':'Email'}),
            'phone_number': TextInput(attrs={'placeholder':'Phone Number'}),
        }
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = PasswordInput(attrs={'placeholder': 'Password'})
        self.fields['password2'].widget = PasswordInput(attrs={'placeholder': 'Confirm Password'})

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('first_name','last_name','username','email','phone_number')
        widgets = {
            'first_name': TextInput(attrs={'placeholder':'First Name'}),
            'last_name': TextInput(attrs={'placeholder':'Last Name'}),
            'username': TextInput(attrs={'placeholder':'Username'}),
            'email': EmailInput(attrs={'placeholder':'Email','readonly':'True'}),
            'phone_number': TextInput(attrs={'placeholder':'Phone Number','readonly':'True'}),
        }

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=PasswordInput(attrs={'placeholder':'Old Password'}))
    new_password1 = forms.CharField(widget=PasswordInput(attrs={'placeholder':'New Password'}))
    new_password2 = forms.CharField(widget=PasswordInput(attrs={'placeholder':'Confirm Password'}))
    
    class Meta:
        model = CustomUser

    # def __init__(self, user, *args, **kwargs):
    #     super(PasswordChangeForm, self).__init__(self, user, *args, **kwargs)
    #     self.fields['old_password'].widget = TextInput(attrs={'placeholder': 'Old Password'})
    #     self.fields['new_password1'].widget = TextInput(attrs={'placeholder': 'New Password'})
    #     self.fields['new_password2'].widget = PasswordInput(attrs={'placeholder': 'Confirm Password'})
