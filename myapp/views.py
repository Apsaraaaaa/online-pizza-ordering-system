from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Pizza, Order, Customer

# Home page
def home(request):
    pizzas = Pizza.objects.all()
    return render(request, 'myapp/home.html', {'pizzas': pizzas})

# Menu page
def menu(request):
    pizzas = Pizza.objects.all()
    return render(request, 'myapp/menu.html', {'pizzas': pizzas})

def cart(request):
    cart = request.session.get('cart', [])
    pizzas = Pizza.objects.filter(id__in=cart)
    total = sum([p.calculate_total() for p in pizzas])
    return render(request, 'myapp/cart.html', {'pizzas': pizzas, 'total': total})

# Add to cart
def add_to_cart(request, pizza_id):
    cart = request.session.get('cart', [])
    cart.append(pizza_id)
    request.session['cart'] = cart
    return redirect('cart')

# Checkout page
def checkout(request):
    cart = request.session.get('cart', [])
    pizzas = Pizza.objects.filter(id__in=cart)
    total = sum([p.calculate_total() for p in pizzas])

    if request.method == 'POST':
        customer, _ = Customer.objects.get_or_create(email=request.POST['email'], defaults={
            'name': request.POST['name'],
            'phone': request.POST['phone']
        })
        order = Order.objects.create(customer=customer, total_price=total)
        order.pizzas.set(pizzas)
        order.save()
        request.session['cart'] = []  # clear cart
        return redirect('orders')

    return render(request, 'myapp/checkout.html', {'pizzas': pizzas, 'total': total})


# User login
def user_login(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            return redirect('home')
    return render(request, 'myapp/login.html')

# User logout
def user_logout(request):
    logout(request)
    return redirect('home')

# User register
def register(request):
    if request.method == 'POST':
        user = User.objects.create_user(
            username=request.POST['username'],
            email=request.POST['email'],
            password=request.POST['password']
        )
        login(request, user)
        return redirect('home')
    return render(request, 'myapp/register.html')
