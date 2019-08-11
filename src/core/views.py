from django.shortcuts import render
from .models import Item

def item_list(request):
    items = Item.objects.all()
    contex = {
        'items': items
    }
    return render(request, "home-page.html", contex)

def checkout(request):
    return render(request, 'checkout-page.html', {})

def products(request):
    return render(request, 'product-page.html', {})

