# from django.contrib.auth.decorators import *
# from django.http import request
# from django.shortcuts import render
# from django.contrib import messages
# from tracker.models import Product

# def premium_required(function=None, login_url=None, redirect_field_name=None, raise_exception=False):
#     """
#     check if user is premium user or not.
#     """
#     products_count = Product.objects.filter(user=request.user).count()

#     def check_premium(user):
#         if user.is_premiun:
#             messages.error(request, 'You are not a premium user. buy premium account to be able to add more products.')
#             return render(request, '/tracking-list/')
#         else:
#             return True

#     return user_passes_test(check_premium, login_url=login_url)