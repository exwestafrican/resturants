from django.contrib import admin
from cart.forms import CartItemForm
from cart.models import CartItem, Cart
from products.utils import random_generator

# Register your models here.


class CartItemAdmin(admin.ModelAdmin):
    list_display = (
        "cart",
        "product",
    )
    # search_fields = ['owner']
    readonly_fields = ["item_total", "created", "anonymous_cart_id"]
    raw_id_fields = ["product"]
    form = CartItemForm

    # list_per_page = 2

    def item_total(self, obj):
        return obj.item_total

    # def save_model(*args,**kwargs):
    #     print('Admin args',args)
    #     print('Admin kwargs',kwargs)
    #     super().save_model(*args,**kwargs)


# set owner as request.user overide save function


class CartAdmin(admin.ModelAdmin):
    # form = CartForm
    readonly_fields = ["cart_id", "total", "session_id"]


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)

