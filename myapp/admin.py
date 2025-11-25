from django.contrib import admin
from .models import Customer, CustomerProfile, Topping, PizzaSize, PizzaCrust, Pizza, Order

admin.site.register(Customer)
admin.site.register(CustomerProfile)
admin.site.register(Topping)
admin.site.register(PizzaSize)
admin.site.register(PizzaCrust)
admin.site.register(Pizza)
admin.site.register(Order)
