from django.urls import path
from . import api_views

urlpatterns = [
    path('pizzas/', api_views.pizza_list, name='pizza-list'),
    path('pizzas/<int:pk>/', api_views.pizza_detail, name='pizza-detail'),
    
]
