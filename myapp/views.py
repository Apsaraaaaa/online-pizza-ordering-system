from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from .models import Pizza, Order, Customer
def home(request):
    special_pizzas = Pizza.objects.all()[:4]  
    return render(request, 'myapp/home.html', {'special_pizzas': special_pizzas})

def menu(request):
    pizzas = Pizza.objects.all()
    return render(request, 'myapp/menu.html', {'pizzas': pizzas})

def cart(request):
    cart = request.session.get('cart', {}) 
    pizzas_in_cart = []
    total_price = 0

    for pizza_id, qty in cart.items():
        pizza = get_object_or_404(Pizza, id=pizza_id)
        pizza_total = pizza.calculate_total() * qty  
        total_price += pizza_total
        pizzas_in_cart.append({
            'pizza': pizza,
            'quantity': qty,
            'total': pizza_total
        })

    return render(request, 'myapp/cart.html', {
        'pizzas_in_cart': pizzas_in_cart,
        'total_price': total_price
    })

# add_to_cart
def add_to_cart(request, pizza_id):
    cart = request.session.get('cart', {})
    if str(pizza_id) in cart:
        cart[str(pizza_id)] += 1
    else:
        cart[str(pizza_id)] = 1
    request.session['cart'] = cart
    request.session.modified = True
    messages.success(request, "Pizza added to cart!")
    return redirect('menu')  

# remove_from_cart
def remove_from_cart(request, pizza_id):
    cart = request.session.get('cart', {})
    pizza_id = str(pizza_id)
    if pizza_id in cart:
        del cart[pizza_id]      
        request.session['cart'] = cart
        request.session.modified = True
        messages.success(request, "Pizza removed from cart.")
    return redirect('cart')  


# Register
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
            messages.success(request, f"Account created for {username}!")
            return redirect('home')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserCreationForm()

    return render(request, 'myapp/register.html', {'form': form})

# Login
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('home')
        messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'myapp/login.html', {'form': form})

# Logout
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')
