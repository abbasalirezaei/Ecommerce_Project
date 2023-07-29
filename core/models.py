from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model
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
    