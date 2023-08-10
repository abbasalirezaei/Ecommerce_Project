from django.conf import settings
from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django_countries.fields import CountryField
# Get the user model
User = get_user_model()

CATEGORY = (
    ('S', 'Shirt'),
    ('SP', 'Sport Wear'),
    ('OW', 'Out Wear')
)

LABEL = (
    ('N', 'New'),
    ('BS', 'Best Seller')
)
#  Item will store product data
class Item(models.Model) :
    item_name = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY, max_length=2)
    label = models.CharField(choices=LABEL, max_length=2)
    description = models.TextField()

    def __str__(self):
        return self.item_name
    # get_absolute_url will return url from product
    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            "pk" : self.pk
        
        })
    # get_add_to_cart_url will return url to function
    #  add item to cart in views.py file we will make
    def get_add_to_cart_url(self) :
        return reverse("core:add-to-cart", kwargs={
            "pk" : self.pk
        })
    """
    get_remove_from_cart_url will return url to function 
    remove item from cart in views.py file we will make
    """

    def get_remove_from_cart_url(self) :
        return reverse("core:remove-from-cart", kwargs={
            "pk" : self.pk
        })   
    
# OrderItem will store product data that you want to order
class OrderItem(models.Model) :
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)
    """
    get_total_item_price, 
    returns the total price value of each product item
    """
    def get_total_item_price(self):
        return self.quantity * self.item.price
    """
    get_discount_item_price, returns the total price
     value of each product item based on discounted prices
    """
    def get_discount_item_price(self):
        return self.quantity * self.item.discount_price
    """
    get_amount_saved, returns the 
    value of the price saved from existing discounts
    """
    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_discount_item_price()
    """
    get_final_price, returns which function is used as a price determinant 
    (whether using the original price or discounted price)
    """
    def get_final_price(self):
        if self.item.discount_price:
            return self.get_discount_item_price()
        return self.get_total_item_price()   
    def __str__(self):
        return f"{self.quantity} of {self.item.item_name}"

        
#  Order will store order information
class Order(models.Model) :
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    """
    get_total_price, returns the value 
    of the total price of all ordered product items
    """
    def get_total_price(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total


class CheckoutAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

class Payment(models.Model):
    stripe_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, 
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username