from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django_countries.fields import CountryField

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)


class Category(models.Model):
    category = models.CharField(max_length=30)

    def __str__(self):
        return self.category


class Item(models.Model):
    item_name = models.CharField(max_length=100)
    item_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    item_image = models.ImageField(upload_to='items_images/')
    labels = models.CharField(choices=LABEL_CHOICES, max_length=2)
    slug = models.SlugField()

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
    billing_address = models.ForeignKey('BillingAddress', models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey('Payment', models.SET_NULL, blank=True, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total = total + order_item.get_final_price()
        return total


class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=True)
    zip_code = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    stripe_charge_id = models.CharField(max_length=50)
    amount = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)



