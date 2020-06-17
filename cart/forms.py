from django.forms import ModelForm

from cart.models import CartItem


class CartItemForm(ModelForm):
    """
    generates a form to dictate
    how item is created
    """
    class Meta:
        model = CartItem
        fields = ['cart','product','quantity','owner','amount']
        