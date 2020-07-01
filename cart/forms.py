from django.forms import ModelForm

from cart.models import CartItem,Cart


class CartItemForm(ModelForm):
    """
    generates a form to dictate
    how item is created
    """
    class Meta:
        model = CartItem
        fields = ['cart','product','quantity']






  


        