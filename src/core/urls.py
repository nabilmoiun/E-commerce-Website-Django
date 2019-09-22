from django.urls import path
from .views import checkout, HomeView, ItemDetailView, add_to_cart, remove_from_the_cart

app_name = 'core'

urlpatterns = [
    path('item_list/', HomeView.as_view(), name ='item_list'),
    path('checkout/', checkout, name='checkout'),
    path('products/<slug>/', ItemDetailView.as_view(), name='products'),
    path('add_to_cart/<slug>/',add_to_cart, name='add_to_cart'),
    path('remove_from_the_cart/<slug>/',remove_from_the_cart, name='remove_from_the_cart'),

]