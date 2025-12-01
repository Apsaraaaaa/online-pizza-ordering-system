from django.db import models
from decimal import Decimal

from django.contrib.auth.models import User



class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name



class CustomerProfile(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    address = models.TextField()
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profile of {self.customer.name}"




class Topping(models.Model):
    name = models.CharField(max_length=50)
    extra_price = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return self.name


class PizzaSize(models.Model):
    name = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name


class PizzaCrust(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Pizza(models.Model):
    name = models.CharField(max_length=100)
    size = models.ForeignKey(PizzaSize, on_delete=models.PROTECT)
    crust = models.ForeignKey(PizzaCrust, on_delete=models.PROTECT)
    toppings = models.ManyToManyField(Topping, blank=True)
    image = models.ImageField(upload_to='pizzas/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_total(self):
        topping_cost = sum([Decimal(t.extra_price) for t in self.toppings.all()])
        return self.size.price + topping_cost

    def __str__(self):
        return f"{self.name} ({self.size.name})"


class Menu(models.Model):
    name = models.CharField(max_length=100)
    pizzas = models.ManyToManyField(Pizza, blank=True)
    description = models.TextField(blank=True)
    is_special = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def total_items(self):
        return self.pizzas.count()


class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COOKING', 'Cooking'),
        ('DELIVERED', 'Delivered'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    pizzas = models.ManyToManyField(Pizza)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    total_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    ordered_at = models.DateTimeField(auto_now_add=True)

    def calculate_total(self):
        total = sum([p.calculate_total() for p in self.pizzas.all()])
        self.total_price = total
        self.save()
        return self.total_price

    def __str__(self):
        return f"Order #{self.id} by {self.customer.name}"