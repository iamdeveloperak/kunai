from django.urls import path
from . import views
urlpatterns = [
    path('', views.tracking_view, name='tracking-list'),
    path('delete/<int:id>/', views.delete_product, name='delete-product')
]