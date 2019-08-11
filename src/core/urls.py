from django.urls import path
from .views import item_list, checkout, products

urlpatterns = [
    path('item_list/', item_list, name ='item_list'),
    path('checkout/', checkout, name='checkout'),
    path('products/', products, name='products'),
]