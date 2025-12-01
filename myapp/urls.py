from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path("admin/", admin.site.urls),

    # user pages
    path("", views.home, name="home"),
    path("menu/", views.menu, name="menu"),
    path("cart/", views.cart, name="cart"),
    path("add_to_cart/<int:pizza_id>/", views.add_to_cart, name="add_to_cart"),
    path("remove_from_cart/<int:pizza_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
    path("order-now/", views.order_now, name="order_now"),

    #admin pages
path("admin-login/", views.admin_login, name="admin_login"),
path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
path("admin-orders/", views.admin_orders, name="admin_orders"),
path("confirm-order/<int:order_id>/", views.confirm_order, name="confirm_order"),
path("delete-pizza/<int:pizza_id>/", views.delete_pizza_admin, name="delete_pizza_admin"),
path("admin-logout/", views.admin_logout, name="admin_logout"),
]
