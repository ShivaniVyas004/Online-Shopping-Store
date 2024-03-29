from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=200)
    warehouse = models.CharField(max_length=100, null=False, blank=False, default='Windsor')

    def __str__(self):
        return 'Category: ' + self.name

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=100,
        validators=[
        MaxValueValidator(1000),
        MinValueValidator(0)]
    )
    available = models.BooleanField(default=True)
    description = models.TextField(max_length=200, null=True, blank=True,default=True)
    interested = models.PositiveIntegerField(default=0)

    def __str__(self):
        return 'Product: ' + self.name

    def refill(self):
        self.stock = self.stock+100
        return self.stock


class Client(User):
    PROVINCE_CHOICES = [
        ('AB', 'Alberta'),
        ('MB', 'Manitoba'),
        ('ON', 'Ontario'),
        ('QC', 'Quebec'),
    ]

    company = models.CharField(max_length=50, null=True, blank=True)
    shipping_address = models.CharField(max_length=300, null=True, blank=True)
    city = models.CharField(max_length=20, default='Windsor')
    province=models.CharField(max_length=2, choices=PROVINCE_CHOICES, default='ON')
    interested_in = models.ManyToManyField(Category)


    def __str__(self):
        return 'Client: ' + self.username

class Order(models.Model):
    ORDER_CHOICES = [
        (0, 'Order Cancelled'),
        (1, 'Order Placed'),
        (2, 'Order Shipped'),
        (3, 'Order Delivered'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    num_units = models.PositiveIntegerField(default=100)
    order_status = models.IntegerField(choices= ORDER_CHOICES, default=1)
    status_date = models.DateField(default=datetime.date.today)

    def total_cost(self):
        return self.product.price * self.num_units

    def __str__(self):
        return 'Order: ' + self.product.name