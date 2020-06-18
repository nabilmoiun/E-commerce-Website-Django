from django.contrib import admin
from .models import Item, OrderItem, Cart, BillingAddress

admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Cart)
admin.site.register(BillingAddress)
