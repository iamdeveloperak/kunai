from django.shortcuts import render, redirect
import requests
from .forms import ProductForm
from .models import Product
from django.contrib.auth.decorators import login_required
from .utils import getproduct
from django.contrib import messages
from django.conf import settings
from website.models import SiteMeta, Page
import urllib3
http = urllib3.PoolManager()

# Create your views here.

@login_required
def tracking_view(request):
    sitedata = SiteMeta.objects.first()
    pagedata = Page.objects.filter(page_name="tracking-list").first()
    context = {
        'sitedata': sitedata, 
        'pagedata': pagedata,
        'active': 'tracking-list'
    }
    form = ProductForm()
    if request.method == 'POST':
        products_count = Product.objects.filter(user=request.user).count()
        print(products_count)
        if (products_count < 3 and not request.user.is_premium_user) or (products_count >= 3 and request.user.is_premium_user):
            form = ProductForm(data=request.POST)
            if form.is_valid():
                link = form.cleaned_data.get('link')

                # scrape product
                product_data = getproduct(link)
                product = Product()
                product.image = product_data['image_url']
                try:
                    imagefile = open(settings.MEDIA_ROOT + '\\' + product_data['image_name'], "wb")
                    imagefile.write(http.request('GET',product_data['image_url']).data)
                    imagefile.close()
                    product.image = product_data['image_name']
                except:
                    print(product_data['image_url'])
                    product.image = product_data['image_url']
                
                # save product in database
                product.link = product_data['url']
                product.title = product_data['title']
                product.price = product_data['price']
                product.availability = product_data['availability']
                if product.deal_price !=0:
                    product.deal_price = product_data['deal_price']
                    product.on_sale = True
                product.user = request.user
                product.save()
                messages.success(request, 'Product has been added to the tracking list.')
                form = ProductForm()
            else:
                messages.error(request, 'Link is not valid.')
        else:
            messages.error(request, 'You are not a premium user. buy premium account to be able to add more products.')

    context['form'] = form
    context['products'] = Product.objects.filter(user=request.user)

    return render(request, 'tracking-list.html', context)

@login_required
def delete_product(request, id=id):
    form = ProductForm()
    instance = Product.objects.get(id=id)
    instance.image.storage.delete(str(instance.image))
    instance.delete()
    return redirect('/tracking-list/')