from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path("admin/", admin.site.urls),

    # Public pages
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('cart/', views.cart, name='cart'),
    path('order-form/', views.order_now, name='order_form'),  

    # Cart actions
    path('add-to-cart/<int:pizza_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:pizza_id>/', views.remove_from_cart, name='remove_from_cart'),

    # Authentication
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Admin
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-orders/', views.admin_orders, name='admin_orders'),
    path('delete-order/<int:order_id>/', views.delete_order, name='delete_order'),
    path('edit-pizza/<int:pizza_id>/', views.edit_pizza, name='edit_pizza'),
    path('delete-pizza/<int:pizza_id>/', views.delete_pizza_admin, name='delete_pizza_admin'),
]
