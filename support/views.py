from django.shortcuts import render, HttpResponseRedirect
from website.models import SiteMeta, Page
from .forms import SupportForm
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.core.mail import send_mail
from kunai import settings
# Create your views here.

def support(request):
    sitedata = SiteMeta.objects.first()
    pagedata = Page.objects.filter(page_name="support").first()
    if request.method == 'POST':
        form = SupportForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            from_email = 'kunaitrackerapp@gmail.com'

            message = render_to_string('emails/support_email.html',{
                'name': name,
                'email': email,
                'phone': phone,
                'subject': subject,
                'message': message,
            })

            try:
                send_mail(
                    subject=subject, 
                    from_email=settings.EMAIL_HOST_USER, 
                    recipient_list=[settings.EMAIL_HOST_USER,], 
                    fail_silently=False,
                    message=message,
                    html_message=message,
                )
            except Exception as e:
                print('--unable to send the support email', e)            
            form.save()
            return HttpResponseRedirect('/thankyou/')
    else:
        form = SupportForm()
    data = {
        'sitedata': sitedata,
        'pagedata': pagedata,
        'form': form,
        'active': 'support'
    }
    return render(request, 'support.html', data)