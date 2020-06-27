from django.urls import path

from .views import (HomeView, ItemDetailView, add_to_cart, remove_from_the_cart, OrderSummary,
                    remove_single_from_the_cart, CheckoutView, PaymentView, AddCouponView,
                    RequestRefundView, add_likes_to_product)

app_name = 'core'

urlpatterns = [
    path('',
         HomeView.as_view(), name='item_list'),
    path('item_list/<category_name>/',
         HomeView.as_view(), name='item_list_by_category'),
    path('checkout/',
         CheckoutView.as_view(), name='checkout'),
    path('payment/<payment_option>/',
         PaymentView.as_view(), name="payment"),
    path('products/<slug>/',
         ItemDetailView.as_view(), name='products'),
    path('order_summary/',
         OrderSummary.as_view(), name='order_summary'),
    path('add_to_cart/<slug>/',
         add_to_cart, name='add_to_cart'),
    path('remove_from_the_cart/<slug>/',
         remove_from_the_cart, name='remove_from_the_cart'),
    path('remove_single_from_the_cart/<slug>/',
         remove_single_from_the_cart, name='remove_single_from_the_cart'),
    path('add_coupon/',
         AddCouponView.as_view(), name="add_coupon"),
    path('request_refund/',
         RequestRefundView.as_view(), name="request_refund"),
    path('add_likes_to_product/<slug>/',
         add_likes_to_product, name="likes")
]
