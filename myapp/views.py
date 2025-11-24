from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from .models import Pizza, Order, Customer

# Home page
def home(request):
    pizzas = Pizza.objects.all()
    return render(request, 'myapp/home.html', {'pizzas': pizzas})

# Menu page
def menu(request):
    pizzas = Pizza.objects.all()
    return render(request, 'myapp/menu.html', {'pizzas': pizzas})

# Cart page
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
        customer, _ = Customer.objects.get_or_create(
            email=request.POST['email'],
            defaults={'name': request.POST['name'], 'phone': request.POST['phone']}
        )
        order = Order.objects.create(customer=customer, total_price=total)
        order.pizzas.set(pizzas)
        order.save()
        request.session['cart'] = []  # clear cart after checkout
        return redirect('orders')

    return render(request, 'myapp/checkout.html', {'pizzas': pizzas, 'total': total})

# Register view
def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserCreationForm()

    return render(request, 'myapp/register.html', {'form': form})

# Login view
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm()

    return render(request, 'myapp/login.html', {'form': form})

# Logout view
def logout_view(request):
    logout(request)
    return redirect('home')
