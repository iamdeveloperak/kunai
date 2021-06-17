from django.urls import path
from django.urls.resolvers import URLPattern
from . import views
urlpatterns = [
    path('', views.membership),
    path('<slug:slug>/', views.payment),
    # path('handlerequest/', views.handlerequest, name = 'handlerequest'),
]