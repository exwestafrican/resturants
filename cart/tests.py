from django.test import TestCase

# Create your tests here.


from django.contrib.auth import get_user_model
from django.contrib.auth import get_user_model
from cart.models import Cart,CartItem
from products.models import ProductVariation

cart = Cart.objects.first()
user = get_user_model().objects.first()
product = ProductVariation.objects.first()
cart = Cart.objects.create(total=350,owner=user)
cart.cart_id


#test adding excess items to cart
user = get_user_model().objects.first()
product = ProductVariation.objects.first()
cart = Cart.objects.create(owner=user)
add_item_to_cart = CartItem.objects.create(cart=cart,product=product,quantity=200)


#testing unique together constrainst for cart and prodict
user = get_user_model().objects.first()
product = ProductVariation.objects.first()
cart = Cart.objects.create(owner=user)
add_item_to_cart = CartItem.objects.create(cart=cart,product=product,quantity=2)




from cart.models import Cart,CartItem
cart = Cart.objects.get(cart_id="crc8r399")
cart.cart_items.all()
a=[ item.item_total for item in cart.cart_items.all()]
sum(a)