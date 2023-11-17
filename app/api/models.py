import decimal
from django.db import models


class Category (models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name

class Item (models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=4)
    vat_rate = models.DecimalField(max_digits=4, decimal_places=4, null=True, default=0.16)
    created_at_utc = models.DateTimeField(auto_now_add=True)

    @property
    def price_with_tax(self):
        return self.price * (1 + self.vat_rate)

    def __str__(self):
        return f"{self.name} - {self.description}: {self.price}"
    
class Client (models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=11)
    address = models.CharField(max_length=100)
    country_code = models.CharField(max_length=2)
    created_at = models.DateTimeField(auto_now_add=True)
    reduced_vat_rate = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.name}"
    
class Order (models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    client = models.ForeignKey(Client, on_delete=models.RESTRICT)
    items = models.ManyToManyField(Item, through='OrderItem')
    created_at = models.DateTimeField(auto_now_add=True)
    cancelled_at = models.DateTimeField(null=True)
    cancelled = models.BooleanField(default=False)
    status = models.CharField(max_length=100, default='PENDING')

    @property
    def vat(self):
        tax = 0
        for order_item in OrderItem.objects.filter(order_id=self.id):
            tax += order_item.vat
        return tax

    @property
    def subtotal(self):
        subtotal = 0
        for order_item in OrderItem.objects.filter(order_id=self.id):
            subtotal += order_item.subtotal
        return subtotal
    
    @property
    def total(self):
        return self.subtotal + self.vat
    
    def __str__(self):
        return f"{self.client.name}: {self.items} - {self.created_at}"
    
class OrderItem (models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    order = models.ForeignKey(Order, on_delete=models.RESTRICT)
    item = models.ForeignKey(Item, on_delete=models.RESTRICT)
    quantity = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=4)
    vat = models.DecimalField(max_digits=10, decimal_places=4)

    @property
    def unit_price(self):
        return self.subtotal / self.quantity

    @property
    def total(self):
        return self.subtotal + self.vat

    def __str__(self):
        return f"{self.order} - {self.item} - {self.quantity} - {self.created_at}"