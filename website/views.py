from django.shortcuts import render
from .models import SiteMeta, Page, PageSection, InfoCard
from django.contrib.auth.decorators import login_required
# Create your views here.
# sitedata = SiteMeta.objects.first()
def index(request):
    sitedata = SiteMeta.objects.first()
    pagedata = Page.objects.filter(page_name="index").first()
    sectiondata = PageSection.objects.get(title__icontains="amazing features")
    data = {
        'sitedata': sitedata, 
        'pagedata': pagedata, 
        'afsection': sectiondata,
        'active': 'home'
    }
    return render(request, 'index.html', data)

@login_required
def tracking_list(request):
    sitedata = SiteMeta.objects.first()
    data = {'sitedata': sitedata, 'active': 'tracking-list'}
    return render(request, 'tracking-list.html', data)

def privacyterms(request):
    sitedata = SiteMeta.objects.first()
    context = {
        'sitedata': sitedata, 
    }
    return render(request, 'terms/privacyterms.html', context)

def privacypolicy(request):
    sitedata = SiteMeta.objects.first()
    context = {
        'sitedata': sitedata, 
    }
    return render(request, 'terms/privacypolicy.html', context)

def termsandconditions(request):
    sitedata = SiteMeta.objects.first()
    context = {
        'sitedata': sitedata, 
    }
    return render(request, 'terms/termsandconditions.html', context)