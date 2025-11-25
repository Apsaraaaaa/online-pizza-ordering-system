from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from .models import Pizza, Order, Customer

def home(request):
    pizzas = Pizza.objects.all()
    return render(request, 'myapp/home.html', {'pizzas': pizzas})

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


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')