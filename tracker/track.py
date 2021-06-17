from .models import Product
from .utils import getproduct
from django.template.loader import render_to_string
from django.core.mail import send_mail
from kunai import settings

def product_notification_mail(product, email_subject, user_message):
    to_email = product.user.email
    message = render_to_string('emails/product_notification_email.html',{
            'product': product,
            'user_message': user_message,
        })
    try:
        send_mail(
            subject= email_subject,
            message= message,
            from_email= settings.EMAIL_HOST_USER,
            recipient_list= [to_email],
            fail_silently= False,
            html_message = message,
        )
    except Exception as e:
        print('--unable to send the product notification email', e)

def update_data(product, data):

    try:
        if data['availability'] == 'unavailable':
            product.availability = data['availability']
            product.price = 0
            product.changed_price = 0
            product.deal_price = 0
            product.redused_price = 0
            product.on_sale = False
        elif product.availability == 'unavailable' and data['availability'] == 'available':
            if data['price'] > 0:
                product.availability = data['availability']
                product.price = data['price']
                product.changed_price = 0
                product.deal_price = 0
                product.redused_price = 0
                product.on_sale = False
                #product came in stock
                product_notification_mail(product, 'The product you were looking for just came in stock.', "The product you were looking for just came in stock.")
            elif data['deal_price'] > 0 and data['price'] == 0:
                product.availability = data['availability']
                product.price = data['deal_price']
                product.changed_price = 0
                product.deal_price = data['deal_price']
                product.redused_price = 0
                product.on_sale = True
                #product from unavailable to in deal
                product_notification_mail(product, 'The product you were looking for just came in stock And deal is going on.', "The product you were looking for just came in stock and a deal is going on.")
            else:
                pass
        elif product.availability != 'unavailable' and data['availability'] != 'unavailable':
            if data['price'] > 0:
                if (data['price'] > product.price and product.changed_price == 0) or (data['price'] > product.changed_price and product.changed_price > 0):
                    product.availability = data['availability']
                    #product.price = data['price']
                    product.changed_price = data['price']
                    product.deal_price = 0
                    product.redused_price = 0
                    product.on_sale = False
                    #price increased
                elif (data['price'] < product.price and product.changed_price == 0) or (data['price'] < product.changed_price and product.changed_price > 0):
                    product.availability = data['availability']
                    #product.price = data['deal_price']
                    product.changed_price = data['price']
                    product.deal_price = 0
                    product.redused_price = product.price - data['price']
                    product.on_sale = True
                    #price decreased
                    product_notification_mail(product, 'Wooh! Product Price has decreased. You can buy it now.', "The product's price has been redused.")
                else:
                    pass
            if data['deal_price'] > 0:
                if (data['deal_price'] < product.price and product.deal_price == 0) or (data['deal_price'] < product.deal_price and product.deal_price > 0):
                    product.availability = data['availability']
                    #product.price = data['price']
                    product.changed_price = 0
                    product.deal_price = data['deal_price']
                    product.redused_price = product.price - data['deal_price']
                    product.on_sale = True
                    #product is on deal
                    product_notification_mail(product, 'Wooh! Deal is going on this product. You can buy it now.', "The product's price has been redused.")
                else:
                    pass
        else:
            pass

        product.save()
        # return product
    except Exception as e:
        print('---EXCEPTION:',e)

def track():
    products = Product.objects.all()

    for product in products:
        new_data = getproduct(product.link)
        update_data(product, new_data)
        # product.save()
        # print(f'{product.id}: Product Updated.')