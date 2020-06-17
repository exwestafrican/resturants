from django.db import models
from django.contrib.auth import get_user_model,settings
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from products.models import ProductVariation
from products.utils import random_generator

from cart.managers import CartItemManager,CartManager
from django.db.models.signals import pre_save
# Create your models here.


User = settings.AUTH_USER_MODEL


class CartItem(models.Model):
    cart        = models.ForeignKey('Cart',on_delete=models.CASCADE)
    product     = models.ForeignKey(ProductVariation,on_delete=models.CASCADE)
    quantity    = models.PositiveIntegerField(default=1)
    owner       = models.ForeignKey(User,on_delete=models.CASCADE) 
    amount      = models.DecimalField(max_digits=10, decimal_places=2,blank=True)
    created     = models.DateTimeField(auto_now_add=True)

    objects    = CartItemManager()


    def __str__(self):
        return f'{self.quantity}units of {self.product}'

    def item_total(self):
       return  self.product.current_price * self.quantity


def get_cart_amount(sender,instance,*args,**kwargs):
    """
    signal updates cart item total 
    anytime a user creates or modifies item.
    """
    if instance.amount is None or instance.amount!=instance.item_total():
        instance.amount = instance.item_total()
        instance.save()

pre_save.connect(get_cart_amount,sender=CartItem)




class Cart(models.Model):
    """
   handles updating 
    total cart cost and attributing it to owner
    """
    cart_id     = models.CharField(max_length=200,blank=True) #alphanumberic string - 5chars long - unique=true 
    owner       = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    total       = models.DecimalField(max_digits=10, decimal_places=2,blank=True,default=0)   
    created     = models.DateTimeField(auto_now_add=True,null=True)
    anonymousId = models.CharField(max_length=200,blank=True,null=True)


    objects = CartManager()

    def __str__(self):
        return self.cart_id

    #use a many to many signal to handle order toal 



    #order summary
    #delivery date - choice field  base impimentation is from timedelta+2days 
