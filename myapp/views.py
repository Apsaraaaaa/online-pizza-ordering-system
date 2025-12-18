from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Pizza, Order, Customer, PizzaSize, PizzaCrust, Topping

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

def order_now(request):
    if request.method == "POST":
        pizza_name = request.POST.get("pizza_name")
        size_id = request.POST.get("size")
        crust_id = request.POST.get("crust")
        topping_ids = request.POST.getlist("toppings")

        size = PizzaSize.objects.get(id=size_id)
        crust = PizzaCrust.objects.get(id=crust_id)

        pizza = Pizza.objects.create(
            name=pizza_name,
            size=size,
            crust=crust,
        )
        pizza.toppings.set(topping_ids)

        
        if request.user.is_authenticated:
            customer, _ = Customer.objects.get_or_create(
                email=request.user.email,
                defaults={"name": request.user.username, "phone": "00000"}
            )
        else:
            customer, _ = Customer.objects.get_or_create(
                email="guest@example.com",
                defaults={"name": "Guest User", "phone": "00000"}
            )

       
        order = Order.objects.create(customer=customer)
        order.pizzas.add(pizza)
        order.calculate_total()

        messages.success(request, "Your order has been placed successfully!")
        return redirect("home")

    context = {
        "sizes": PizzaSize.objects.all(),
        "crusts": PizzaCrust.objects.all(),
        "toppings": Topping.objects.all(),
    }
    return render(request, "myapp/order_form.html", context)

def add_to_cart(request, pizza_id):
    cart = request.session.get('cart', {})
    pizza_id = str(pizza_id)

    cart[pizza_id] = cart.get(pizza_id, 0) + 1

    request.session['cart'] = cart
    request.session['cart_message'] = "Pizza added to cart!"
    return redirect('menu')


def remove_from_cart(request, pizza_id):
    cart = request.session.get('cart', {})
    pizza_id = str(pizza_id)

    if pizza_id in cart:
        del cart[pizza_id]
        request.session['cart_message'] = "Pizza removed from cart."

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



def admin_only(user):
    return user.is_staff or user.is_superuser

def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect("admin_dashboard")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_staff:
                login(request, user)
                return redirect("admin_dashboard")
            else:
                messages.error(request, "You are not allowed to access admin dashboard.")
        else:
            messages.error(request, "Invalid credentials.")
    else:
        form = AuthenticationForm()

    return render(request, "myapp/admin_login.html", {"form": form})

@login_required
@user_passes_test(admin_only)
def admin_dashboard(request):
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='PENDING').count()
    delivered_orders = Order.objects.filter(status='DELIVERED').count()
    pizzas = Pizza.objects.all()
    context = {
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "delivered_orders": delivered_orders,
        "pizzas": pizzas,
    }
    return render(request, "myapp/admin_dashboard.html", context)

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def edit_pizza(request, pizza_id):
    pizza = get_object_or_404(Pizza, id=pizza_id)

    if request.method == "POST":
        pizza.name = request.POST.get("name")
        size_id = request.POST.get("size")
        crust_id = request.POST.get("crust")
        topping_ids = request.POST.getlist("toppings")

        pizza.size = PizzaSize.objects.get(id=size_id)
        pizza.crust = PizzaCrust.objects.get(id=crust_id)
        pizza.save()
        pizza.toppings.set(topping_ids)

        messages.success(request, f"{pizza.name} updated successfully!")
        return redirect("admin_dashboard")

    context = {
        "pizza": pizza,
        "sizes": PizzaSize.objects.all(),
        "crusts": PizzaCrust.objects.all(),
        "toppings": Topping.objects.all(),
    }
    return render(request, "myapp/edit_pizza.html", context)


@login_required
@user_passes_test(admin_only)
def admin_orders(request):
    orders = Order.objects.all().order_by("-id")
    return render(request, "myapp/admin_orders.html", {"orders": orders})

@login_required
@user_passes_test(admin_only)
def confirm_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.status = "DELIVERED"
    order.save()
    messages.success(request, "Order confirmed!")
    return redirect("admin_orders")

@login_required
@user_passes_test(admin_only)
def delete_pizza_admin(request, pizza_id):
    pizza = get_object_or_404(Pizza, id=pizza_id)
    pizza.delete()
    messages.success(request, "Pizza deleted successfully!")
    return redirect("admin_dashboard")

@login_required
def admin_logout(request):
    logout(request)
    return redirect("admin_login")

@login_required
@user_passes_test(admin_only)
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    messages.success(request, f"Order #{order_id} deleted successfully!")
    return redirect("admin_orders")