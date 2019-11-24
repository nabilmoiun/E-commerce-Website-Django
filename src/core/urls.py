from django.urls import path
from .views import (HomeView, ItemDetailView, add_to_cart,
                    remove_from_the_cart, OrderSummary, remove_single_from_the_cart,
                    CheckoutView
                    )

app_name = 'core'

urlpatterns = [
    path('item_list/', HomeView.as_view(), name='item_list'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('products/<slug>/', ItemDetailView.as_view(), name='products'),
    path('order_summary/', OrderSummary.as_view(), name='order_summary'),
    path('add_to_cart/<slug>/', add_to_cart, name='add_to_cart'),
    path('remove_from_the_cart/<slug>/',
         remove_from_the_cart, name='remove_from_the_cart'),
    path('remove_single_from_the_cart/<slug>/',
         remove_single_from_the_cart, name='remove_single_from_the_cart'),

]
