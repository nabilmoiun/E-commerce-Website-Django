from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, Order, OrderItem, BillingAddress
from django.views.generic import ListView, DeleteView, View
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CheckoutForm

class HomeView(ListView):
    model = Item
    template_name = "home-page.html"

class ItemDetailView(DeleteView):
    model = Item
    template_name = "product-page.html"

class OrderSummary(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            contex = {
                'object': order
            }
            return render(self.request, 'order_summary.html', contex)
        except ObjectDoesNotExist:
            messages.error(self.request, "You don't have any order ")
            return redirect(self.request, '/item_list/')
        # print("context is : ", contex)
        # all_items = order.items.all()
        # print("itmes are : ", all_items)
@login_required
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

    return redirect("core:order_summary")
@login_required
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
        return redirect("core:order_summary")
    return redirect("core:order_summary")

@login_required
def remove_single_from_the_cart(request, slug):
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
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item was removed from your cart")
        else:
            messages.info(request, "This item is not in your cart")
            
    else:
        messages.info(request, "You have no order existed")
        return redirect("core:order_summary")
    return redirect("core:order_summary")


class CheckoutView(View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        context = {
            'form': form
        }
        return render(self.request, 'checkout-page.html', context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        # print("request post", self.request.Post)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)

            if form.is_valid():
                street_adress = form.cleaned_data.get('street_adress')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                zip_code = form.cleaned_data.get('zip_code')
                # same_billing_address = form.cleaned_data.get('same_billing_address')
                # save_info = form.cleaned_data.get('save_info')
                payment_option = form.cleaned_data.get('payment_option')
                billing_address = BillingAddress(
                    user = self.request.user,
                    street_address = street_adress,
                    apartment_address = apartment_address,
                    country = country,
                    zip_code = zip_code
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
                # add redirect to selected payment method
                print("the form is valid")
                return redirect("core:checkout")

        except ObjectDoesNotExist:
            messages.error(self.request, "Error ")
            return redirect("core:checkout")
        print("what the hell ")


# def products(request):
#     return render(request, 'product-page.html', {})

