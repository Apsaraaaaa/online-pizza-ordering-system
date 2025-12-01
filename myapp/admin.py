from django.contrib import admin
from django.utils.html import format_html
from .models import Customer, CustomerProfile, Topping, PizzaSize, PizzaCrust, Pizza, Order,Menu

class CustomerProfileInline(admin.StackedInline):
    model = CustomerProfile
    can_delete = False
    verbose_name_plural = 'Profile'

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_special', 'total_items', 'created_at')
    list_filter = ('is_special', 'created_at')
    search_fields = ('name',)
    filter_horizontal = ('pizzas',)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'is_active')
    search_fields = ('name', 'email', 'phone')
    inlines = [CustomerProfileInline]

@admin.register(Topping)
class ToppingAdmin(admin.ModelAdmin):
    list_display = ('name', 'extra_price')
    search_fields = ('name',)

@admin.register(PizzaSize)
class PizzaSizeAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')

@admin.register(PizzaCrust)
class PizzaCrustAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Pizza)
class PizzaAdmin(admin.ModelAdmin):
    list_display = ('name', 'size', 'crust', 'image_tag', 'calculate_total', 'created_at')
    list_filter = ('size', 'crust', 'created_at')
    search_fields = ('name',)
    filter_horizontal = ('toppings',)

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" />'.format(obj.image.url))
        return "-"
    image_tag.short_description = 'Image'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'status', 'total_price', 'ordered_at')
    list_filter = ('status', 'ordered_at')
    search_fields = ('customer__name', 'customer__email', 'customer__phone')
    filter_horizontal = ('pizzas',)
    readonly_fields = ('total_price', 'ordered_at')

    def save_model(self, request, obj, form, change):
        """Automatically calculate total when saving an order in admin"""
        super().save_model(request, obj, form, change)
        obj.calculate_total()