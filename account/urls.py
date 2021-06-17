from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetCompleteView, PasswordResetConfirmView
from django.urls import reverse_lazy

urlpatterns = [
    # path('register/', views.custom_user_creation, name="account-register"),
    path('register/', views.SignupViewUser.as_view(), name="account-register"),
    path('login/', views.LoginViewUser.as_view(redirect_authenticated_user=True), name="account-login"),
    path('logout/', views.logout_view, name="account-logout"),
    path('account-settings/', login_required(views.UserEditView.as_view()), name="account-settings"),
    path('change-password/', login_required(views.UserPasswordChangeView.as_view(extra_context = {'old_password': 'Old Password'})), name="password-reset"),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('delete-account/<uidb64>', views.delete_account, name='delete-account'),

    # forget password
    # 1
    path('password-reset/', 
        PasswordResetView.as_view(
            template_name = 'password-reset.html', 
            success_url = reverse_lazy('password-reset-done'), 
            subject_template_name = 'emails/password_reset_subject.txt',
            from_email = 'kunaitrackerapp@gmail.com',
            email_template_name = 'emails/forgot_password_email_text.html',
            html_email_template_name = 'emails/forgot_password_email.html',
        ), 
        name='password-reset'),

    # 2
    path('password-reset-done/', 
        PasswordResetDoneView.as_view(
            template_name = 'password-reset-done.html',
        ), 
        name='password-reset-done'),
    
    # 3
    path('password-reset-confirm/<uidb64>/<token>/', 
        PasswordResetConfirmView.as_view(
            template_name = 'password-reset-form.html', 
            success_url = reverse_lazy('password-reset-complete'),
        ), 
        name='password-reset-confirm'),

    # 4
    path('password-reset-complete/', 
        PasswordResetCompleteView.as_view(
            template_name = 'password-reset-complete.html',
        ), 
    name='password-reset-complete'),
]