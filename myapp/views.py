
# Homepage view
from django.shortcuts import render
from .models import Pizza

def home(request):
    return render(request, 'myapp/home.html')

# Menu page view
def menu(request):
    pizzas = Pizza.objects.all()
    return render(request, 'myapp/menu.html', {"pizzas": pizzas})

# Cart page view
def cart(request):
    global cart_data
    if request.method == "POST":
        pizza = Pizza.objects.get(id=request.POST["pizza_id"])
        cart_data.append({"name": pizza.name, "price": pizza.calculate_total()})
    return render(request, 'myapp/cart.html', {"cart": cart_data})

# Checkout page view
def checkout(request):
    global cart_data
    cart_data = []  # clear cart after checkout
    return render(request, 'myapp/checkout.html')
