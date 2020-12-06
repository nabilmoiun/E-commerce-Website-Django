from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from django.shortcuts import reverse

from django_countries.fields import CountryField

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping')
)


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=20, blank=True, null=True)
    on_click_purchasing = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    category = models.CharField(max_length=30)

    def __str__(self):
        return self.category

    def get_absolute_url(self):
        return reverse("core:item_list_by_category", kwargs={
            "category_name": self.category
        })


class Item(models.Model):
    item_name = models.CharField(max_length=100)
    item_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    item_image = models.ImageField(upload_to='items_images/')
    labels = models.CharField(choices=LABEL_CHOICES, max_length=2)
    slug = models.SlugField(unique=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    description = models.TextField()

    def __str__(self):
        return self.item_name

    def get_absolute_url(self):
        return reverse('core:products', kwargs={
            'slug': self.slug
        })

    def get_add_to_cart(self):
        return reverse('core:add_to_cart', kwargs={
            'slug': self.slug
        })

    def remove_from_the_cart(self):
        return reverse('core:remove_from_the_cart', kwargs={
            'slug':self.slug
        })


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} of {self.item.item_name}"

    def get_total_price(self):
        return self.item.price * self.quantity
    
    def get_total_discount_price(self):
        return self.item.discount_price * self.quantity

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_price()
        else:
            return self.get_total_price()


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    billing_address = models.ForeignKey('Address', related_name='billing_address',
                                        on_delete=models.SET_NULL, blank=True, null=True)
    shipping_address = models.ForeignKey('Address', related_name='shipping_address',
                                         on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey('Payment', models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey('Coupon', models.SET_NULL, blank=True, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    reference_code = models.CharField(max_length=20)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total = total + order_item.get_final_price()
        if self.coupon is not None:
            total -= self.coupon.amount
        return total


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=True)
    zip_code = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    stripe_charge_id = models.CharField(max_length=50, null=True, blank=True)
    ssl_charge_id = models.CharField(max_length=50, null=True, blank=True)
    amount = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)


class Coupon(models.Model):
    coupon = models.CharField(max_length=30)
    amount = models.IntegerField()

    def __str__(self):
        return self.coupon


class Refund(models.Model):
    order = models.ForeignKey(Cart, on_delete=models.CASCADE)
    reference_code = models.CharField(max_length=20)
    reason = models.TextField()
    email = models.EmailField()

    def __str__(self):
        return str(self.pk)


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment


def user_profile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        user_profile = UserProfile.objects.create(user=instance)


# Signal to create user profile every time a new user is created
post_save.connect(user_profile_receiver, sender=settings.AUTH_USER_MODEL)
