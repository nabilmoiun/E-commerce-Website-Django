from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, Cart, OrderItem, BillingAddress
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
    paginate_by = 2


class ItemDetailView(DeleteView):
    model = Item
    template_name = "product-page.html"


class OrderSummary(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Cart.objects.get(user=self.request.user, ordered=False)
            contex = {
                'object': order
            }
            return render(self.request, 'order_summary.html', contex)
        except ObjectDoesNotExist:
            messages.error(self.request, "You don't have any order ")
            return redirect(self.request, '/item_list/')


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    """
    Get the instance of the ordered item from the OrderItem model if it exists otherwise create the instance 
    get_or_create() returns a tuple of (object, created), where object is the retrieved or created object and created 
    is a boolean specifying whether a new object was created.
    """
    ordered_item, is_created = OrderItem.objects.get_or_create(
        user=request.user,
        item=item,
        ordered=False
    )
    user_cart = Cart.objects.filter(user=request.user, ordered=False)
    if user_cart.exists():
        user_order = user_cart[0]
        filtered_user_cart_by_the_ordered_item = user_order.items.filter(item__slug=item.slug)
        """
        If the item is already in the user cart list just increase the item quantity in the OrderItem model
        And you don't have to worry about the update of quantity in the user items field in the Cart model
        As items field in the Cart model has ManyToMany relation to the item field of the OrderItem
        It will automatically update the value in the Cart model in the user item field
        """
        if filtered_user_cart_by_the_ordered_item.exists():
            ordered_item.quantity += 1
            ordered_item.save()
            messages.info(request, "The quantity was updated")
        else:
            user_order.items.add(ordered_item)

    # If user does not have any item in the cart create the new instance in the Order model
    else:
        new_order = Cart.objects.create(
            user=request.user,
            ordered_data=timezone.now(),
        )
        new_order.items.add(ordered_item)
        messages.info(request, "The item was added to the cart")
    return redirect("core:order_summary")


@login_required
def remove_from_the_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Cart.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
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
    order_qs = Cart.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity == 1:
                order.items.remove(order_item)
                order_item.delete()
            else:
                order_item.quantity -= 1
                order_item.save()
                print("current item quantity", order_item.quantity)
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
            order = Cart.objects.get(user=self.request.user, ordered=False)

            if form.is_valid():
                street_address = form.cleaned_data.get('street_adress')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                zip_code = form.cleaned_data.get('zip_code')
                # same_billing_address = form.cleaned_data.get('same_billing_address')
                # save_info = form.cleaned_data.get('save_info')
                payment_option = form.cleaned_data.get('payment_option')
                billing_address = BillingAddress(
                    user=self.request.user,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    country=country,
                    zip_code=zip_code
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

