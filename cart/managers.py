from django.db import models
from products.utils import random_generator
from products.models import Product


class CartItemQuerySet(models.query.QuerySet):
	pass


class CartItemManager(models.Manager):
    def get_queryset(self):
        return CartItemQuerySet(self.model, using=self._db)
    
    def create(self,**field_name):
        """
        handels the creation of a cart items
        ands servers as an extra layer of check
        to ensure product available is not 
        greater than attempted order.
        """
        # print('field_name',field_name)
        cart          = field_name.get('cart')
        quantity      = field_name.get('quantity')
        product       = field_name.get('product')
        
        
        #use model validators for this
        if quantity > product.quantity_available: raise NotImplementedError #add a better form of error message
        #use define clean ref: 
        # product_price = product.price
        # amount        = product_price*quantity
        
        new_cart_item = self.model(**field_name)
        new_cart_item.save()
        #updates quantity of product available with signal after creating cart item? or do it here? 
        #post save remove quantity from total product avaialble
        #post delete add quantity total product available
        return new_cart_item
        

class CartQuerySet(models.query.QuerySet):
	pass

class CartManager(models.Manager):
    def get_queryset(self):
        return CartQuerySet(self.model, using=self._db)
    
    def create(self,**field_name):
        new_cart = self.model(**field_name)
        new_cart.save()
        return new_cart
 
 