from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomUserChangeForm, CustomPasswordChangeForm
from .models import CustomUser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.contrib import messages
from django.urls import reverse_lazy
# email imports
from kunai import settings
from django.core.mail import send_mail, EmailMessage
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from website.models import SiteMeta
from website.views import index
from membership.models import UserMembership, Subscription
# Create your views here.

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("/account/login/")

class LoginViewUser(LoginView):
    template_name = "login.html"

class UserEditView(generic.UpdateView):
    form_class = CustomUserChangeForm
    template_name = 'account-settings.html'
    success_url = '/account/account-settings/'

    def get_object(self):
        return self.request.user

    def get_context_data(self,*args, **kwargs):
        context = super(UserEditView, self).get_context_data(*args,**kwargs)
        usermembership = UserMembership.objects.get(user=self.request.user)
        try:
            subscription = Subscription.objects.get(user_membership=usermembership)
        except:
            subscription = None
        sitedata = SiteMeta.objects.first()
        context['sitedata'] =  sitedata
        context['active'] =  'account-settings'
        context['user'] = self.request.user
        context['usermembership'] = usermembership
        context['subscription'] = subscription
        context['user_pk'] =  urlsafe_base64_encode(force_bytes(self.request.user.pk))
        return context

class SignupViewUser(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = 'register.html'
    success_url = '/account/login/'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        self.object = None
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            u = CustomUser.objects.get(email = request.POST.get('email'))
            if u.is_active == False:
                u.delete()
        except:
            pass
        response = super().post(request, *args, **kwargs)
        user_email = request.POST.get('email')

        if response.status_code == 302:
            user = CustomUser.objects.get(email = user_email)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            mail_subject = 'Activate Your Email.'
            message = render_to_string('emails/acc_active_email.html',{
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = user_email
            form = self.get_form()
            try:
                send_mail(
                    subject= mail_subject,
                    message= message,
                    from_email= settings.EMAIL_HOST_USER,
                    recipient_list= [to_email],
                    fail_silently= False,
                    html_message = message,
                )
                messages.success(request, 'A confirmation email has been sent to your email account. Please click on the link to confirm your account.')
                return self.render_to_response({'form':form})
            except Exception as e:
                # form.add_error('', 'Error occured in sending mail! Please try again.')
                messages.error(request, f'Error occured in sending mail! Please try again. {e}')
                return self.render_to_response({'form':form})
        else:
            return response
    
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist) as e:
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        login(request, user)
        messages.success(request, 'Successfully Logged in!')
        return redirect(reverse_lazy('tracking-list'))
    else:
        return HttpResponse('Activation token is invalid or your account is already verified! Try to login.')

class UserPasswordChangeView(PasswordChangeView):
    template_name = 'change-password.html'
    form_class = CustomPasswordChangeForm
    success_url = '/account/account-settings/'

    def get_context_data(self,*args, **kwargs):
        context = super(UserPasswordChangeView, self).get_context_data(*args,**kwargs)
        sitedata = SiteMeta.objects.first()
        context['sitedata'] =  sitedata
        context['active'] =  'account-settings'
        context['user'] = self.request.user
        return context

def delete_account(request, uidb64):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))   
        user = CustomUser.objects.get(pk=uid)
        user.delete()
        return redirect('/')
    except:
        messages.error(request, "Something Went Wrong!")
        return render(request, '/account/account-settings')