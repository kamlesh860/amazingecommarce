from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.conf import settings
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

# Create your models here.
class register(models.Model):
    fname=models.CharField(max_length=20,null=True,blank=True)
    lname = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=50, null=True, blank=True)
    password = models.IntegerField( null=True, blank=True)

    def __str__(self):
        return self.fname


PRODUCT_COISES=(
    ('s','shirt'),
    ('t','t-shirt'),
    ('j','jeans'),
)


class Item(models.Model):
    img=models.ImageField(upload_to='media')
    title=models.CharField(max_length=30,null=True,blank=True)
    tag=models.CharField(max_length=1,choices=PRODUCT_COISES)
    price=models.FloatField(max_length=5,null=True,blank=True)
    description=models.TextField()


    slug = models.SlugField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_about', kwargs=
            {'slug':self.slug}
        )
    def get_add_to_cart_url(self):
        return reverse('add_to_cart',kwargs=
            {'slug':self.slug})
    
    def get_buynow_url(self):
        return reverse('buynow',kwargs=
            {'slug':self.slug})

   

    
    def get_remove_from_cart_url(self):
        return reverse('remove_from_cart',kwargs=
            {'slug':self.slug})

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item=models.ForeignKey(Item,on_delete=models.CASCADE)
    ordered=models.BooleanField(default=False)
    quantity = models.IntegerField(default=1,null=True,blank=True)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_final_price(self):
        return self.get_total_item_price()

class Order(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    items=models.ManyToManyField(OrderItem)
    start_date=models.DateTimeField(auto_now_add=True)
    ordered_date=models.DateTimeField()
    ordered=models.BooleanField(default=False)


    def __str__(self):
        return self.user.first_name

    def get_total_price(self):
        total=0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total

    def get_total_quantity(self):
        total=0
        for item in self.items.all():
            total +=item.quantity
        return total

class UserDetail(models.Model):

    user_name=models.CharField(max_length=100)
    user_address = models.TextField()
    country=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    zip = models.CharField(max_length=10)
    email = models.EmailField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.user_address

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    img=models.ImageField(default='default.jpg',upload_to='media')
    def __str__(self):
        return f'{self.user.username} Profile'








