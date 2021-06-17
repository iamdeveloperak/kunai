from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from datetime import datetime as dt
from dateutil.relativedelta import relativedelta
import razorpay

from .models import Membership, UserMembership, Subscription, PayHistory
from website.models import SiteMeta, Page, PageSection, InfoCard
from kunai import settings

# Create your views here.

client = razorpay.Client(auth=(settings.razorpay_id, settings.razorpay_account_id))


@login_required
def membership(request):
    if request.user.is_premium_user:
        return HttpResponseRedirect('/')
    sitedata = SiteMeta.objects.first()
    pagedata = Page.objects.filter(page_name="membership").first()
    sectiondata = PageSection.objects.get(title__icontains="pricing")
    membership = Membership.objects.filter(membership_type__icontains="premium")
    data = {
        'sitedata': sitedata, 
        'pagedata': pagedata, 
        'sectiondata': sectiondata,
        'memberships': membership,
        'active': 'membership'
    }
    return render(request, 'membership.html', data)

@login_required
def payment(request, slug):
    if request.method == 'POST':
        callback_url = 'http://' + str(get_current_site(request)) + '/handlerequest/'
        membership = Membership.objects.get(slug=slug)
        usermembership = UserMembership.objects.get(user=request.user)
        usermembership.membership = membership
        print(usermembership)
        notes = {'order-type':'Premium membership'}
        order_currency = 'INR'

        razorpay_order = client.order.create(
            dict(
                amount=int(membership.price*100), 
                currency=order_currency, 
                notes=notes, 
                receipt=usermembership.order_id, 
                payment_capture='0')
        )
        usermembership.order_id = razorpay_order['id']
        usermembership.razorpay_order_id = razorpay_order['id']
        usermembership.save()
        print('razorpay_order_id:',usermembership.razorpay_order_id)

        return render(request, 'payment/paymentsummaryrazorpay.html', {'order': usermembership, 'order_id': razorpay_order['id'], 'orderId': usermembership.order_id, 'price': usermembership.membership.price, 'razorpay_merchant_id': settings.razorpay_id, 'callback_url': callback_url })

    else:
        return HttpResponseRedirect('/membership/')


# for generating pdf invoice
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import os

def fetch_resources(uri, rel):
    path = os.path.join(uri.replace(settings.STATIC_URL, ""))
    return path

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)#, link_callback=fetch_resources)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


from django.core.mail import EmailMultiAlternatives

@csrf_exempt
def handlerequest(request):
    print('handlerequest in process')
    if request.method == "POST":
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            order_id = request.POST.get('razorpay_order_id','')
            signature = request.POST.get('razorpay_signature','')
            params_dict = { 
            'razorpay_order_id': order_id, 
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
            }
            print(params_dict)
            try:
                order_db = UserMembership.objects.get(razorpay_order_id=order_id)
            except:
                print('1')
                return HttpResponse("505 Not Found")
            order_db.razorpay_payment_id = payment_id
            order_db.razorpay_signature = signature
            order_db.save()
            result = client.utility.verify_payment_signature(params_dict)
            print('result :',result)
            if result==None:
                amount = int(order_db.membership.price * 100)   #we have to pass in paisa
                try:
                    # print('payment capture : ',client.payment.capture(payment_id, amount))
                    client.payment.capture(payment_id, amount)
                    order_db.payment_status = 1
                    # order_db.membership_status = 1
                    order_db.user.is_premium = True
                    order_db.user.save()
                    order_db.save()
                    if order_db.membership.duration_period == 'month':
                        Subscription.objects.create(user_membership=order_db, expires_in=dt.now().date() + relativedelta(months=order_db.membership.duration))
                    elif order_db.membership.duration_period == 'year':
                        Subscription.objects.create(user_membership=order_db, expires_in=dt.now().date() + relativedelta(years=order_db.membership.duration))
                    else:
                        pass
                    PayHistory.objects.create(user=order_db.user, payment_for= order_db.membership, date= dt.now().date())
                        
                    return render(request, 'payment/paymentsuccess.html')
                except Exception as e:
                    order_db.payment_status = 2
                    # order_db.membership_status = 0
                    order_db.user.is_premium = False
                    order_db.save()
                    return render(request, 'payment/paymentfailed.html')
            else:
                order_db.payment_status = 2
                # order_db.membership_status = 0
                order_db.user.is_premium = False
                order_db.save()
                return render(request, 'payment/paymentfailed.html')
        except:
            print('2')
            return HttpResponse("505 not found")



## For generating Invoice PDF
                    # template = get_template('payment/invoice.html')
                    # data = {
                    #     'order_id': order_db.order_id,
                    #     'transaction_id': order_db.razorpay_payment_id,
                    #     'user_email': order_db.user.email,
                    #     'date': str(order_db.datetime_of_payment),
                    #     'name': order_db.user.first_name,
                    #     'order': order_db,
                    #     'amount': order_db.membership.price,
                    # }
                    # html  = template.render(data)
                    # result = BytesIO()
                    # pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)#, link_callback=fetch_resources)
                    # pdf = result.getvalue()
                    # filename = 'Invoice_' + data['order_id'] + '.pdf'

                    # mail_subject = 'Recent Order Details'
                    # # message = render_to_string('payment/emailinvoice.html', {
                    # #     'user': order_db.user,
                    # #     'order': order_db
                    # # })
                    # context_dict = {
                    #     'user': order_db.user,
                    #     'order': order_db
                    # }
                    # template = get_template('payment/emailinvoice.html')
                    # message  = template.render(context_dict)
                    # to_email = order_db.user.email
                    # # email = EmailMessage(
                    # #     mail_subject,
                    # #     message, 
                    # #     settings.EMAIL_HOST_USER,
                    # #     [to_email]
                    # # )

                    # # for including css(only inline css works) in mail and remove autoescape off
                    # email = EmailMultiAlternatives(
                    #     mail_subject,
                    #     "hello",       # necessary to pass some message here
                    #     settings.EMAIL_HOST_USER,
                    #     [to_email]
                    # )
                    # email.attach_alternative(message, "text/html")
                    # email.attach(filename, pdf, 'application/pdf')
                    # email.send(fail_silently=False)