from django.test import TestCase

# Create your tests here.


from django.contrib.auth import get_user_model
from django.contrib.auth import get_user_model
from cart.models import Cart,CartItem
from products.models import ProductVariation

cart = Cart.objects.first()
user = get_user_model().objects.first()
product = ProductVariation.objects.first()
cart_item = CartItem.objects.create_cart_item(cart=cart,product=product,quantity=25,owner=user)