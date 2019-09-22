from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, Order, OrderItem
from django.views.generic import ListView, DeleteView
from django.utils import timezone
from django.contrib import messages

class HomeView(ListView):
    model = Item
    template_name = "home-page.html"

class ItemDetailView(DeleteView):
    model = Item
    template_name = "product-page.html"

def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user = request.user,
        ordered = False
        )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        print(order_qs)
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated")
        else:
            order.items.add(order_item)
    else:
        order_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=order_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart")

    return redirect("core:products", slug=slug)

def remove_from_the_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user = request.user,
                ordered = False
        )[0]
            order.items.remove(order_item)
            messages.info(request, "This item was removed from your cart")
        else:
            messages.info(request, "This item is not in your cart")
            
    else:
        messages.info(request, "You have no order existed")
        return redirect("core:products", slug=slug)
    return redirect("core:products", slug=slug)


# def item_list(request):
#     items = Item.objects.all()
#     contex = {
#         'items': items
#     }
#     return render(request, "home-page.html", contex)

def checkout(request):
    return render(request, 'checkout-page.html', {})

# def products(request):
#     return render(request, 'product-page.html', {})

