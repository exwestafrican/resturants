from django.db import models


class CartItemQuerySet(models.query.QuerySet):
	pass


class CartItemManager(models.Manager):
    def get_queryset(self):
        return CartItemQuerySet(self.model, using=self._db)
    
    def create_cart_item(self,**field_name):
        """
        handels the creation of a cart items
        ands servers as an extra layer of check
        to ensure product available is not 
        greater than attempted order.
        """
        cart          = field_name.get('cart')
        owner         =  cart.owner
        quantity      = field_name.get('quantity')
        product       = field_name.get('product')
        if quantity > product.quantity_available: raise NotImplementedError #add a better form of error message

        product_price = product.price
        amount        = product_price*quantity
        return self.model.objects.create(amount=amount,**field_name)
        

class CartQuerySet(models.query.QuerySet):
	pass

class CartManager(models.Manager):
    def get_queryset(self):
        return CartQuerySet(self.model, using=self._db)
    
    def create_cart(self,**field_name):
        cart_id       = random_generator(length=5)#make this unique
        return self.model.objects.create(cart_id=cart_id,**field_name)