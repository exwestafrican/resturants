from django.contrib import admin
from cart.forms import CartItemForm
from cart.models import CartItem,Cart
# Register your models here.

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart','product','owner')
    search_fields = ['owner']
    readonly_fields = ["amount", "created"]
    raw_id_fields = ["product"]
    form = CartItemForm
    # list_per_page = 2

    def save_model(*args,**kwargs):
        print('Admin args',args)
        print('Admin kwargs',kwargs)
        super().save_model(*args,**kwargs)
#set owner as request.user overide save function
   
admin.site.register(Cart)
admin.site.register(CartItem,CartItemAdmin)