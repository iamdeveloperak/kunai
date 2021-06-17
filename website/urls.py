from django.urls import path
from . import views
urlpatterns = [
    path('',views.index, name='index'),
    path('privacyterms/',views.privacyterms, name='privacyterms'),
    path('privacypolicy/',views.privacypolicy, name='privacypolicy'),
    path('termsandconditions/',views.termsandconditions, name='termsandconditions'),
]