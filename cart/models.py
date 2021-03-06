from django.db import models
from django.contrib.auth import get_user_model,settings
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.db.models.signals import pre_save

from products.models import ProductVariation
from products.utils import random_generator

from cart.managers import CartItemManager,CartManager
from django.db.models.signals import pre_save,post_save
# Create your models here.


User = settings.AUTH_USER_MODEL

CART_STATUS = [
    ("shopping","SHOPPING"),
    ("checkout","CHECKOUT"),
    ("paid","PAID"),
    ("cancelled","CANCELLED")
]

class CartItem(models.Model):
    cart        = models.ForeignKey('Cart',related_name='cart_items',on_delete=models.CASCADE)
    product     = models.ForeignKey(ProductVariation,on_delete=models.CASCADE)
    quantity    = models.PositiveIntegerField(default=1)
    # owner       = models.ForeignKey(User,on_delete=models.CASCADE,blank=True)  #not required ?
    created     = models.DateTimeField(auto_now_add=True)

    objects    = CartItemManager()

    #unique together cart and product

    def __str__(self):
        return f'{self.quantity} units of {self.product}'

    @property
    def item_total(self):
       return  self.product.current_price * self.quantity

    @property
    def product_name(self):
        return self.product.product_name

    @property
    def product_price(self):
        return self.product.current_price

   
    def product_available(self):
        return self.product.quantity_available






class Cart(models.Model):
    """
   handles updating 
    total cart cost and attributing it to owner
    """
    cart_id     = models.CharField(max_length=200,blank=True,unique=True,null=True) 
    owner       = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    total       = models.DecimalField(max_digits=10, decimal_places=2,blank=True,default=0)   
    created     = models.DateTimeField(auto_now_add=True,null=True)
    session_id  = models.CharField(max_length=200,blank=True,null=True)
    active      = models.BooleanField(default=True) #keep false till payment is paid
    cart_status = models.CharField(max_length=200,default='shopping',choices=CART_STATUS)
    #updated

    objects = CartManager()

    def __str__(self):
        return str(self.cart_id)

    class Meta:
       ordering = ['-created']

    
    def is_cart_anonymous(self):
        return bool(self.owner)

    #cart is active if it user hasn't paid or cancelled 
    # def update_cart_status(self):
    #     self.bought = True
    #     return self.bought
    


    #use a many to many signal to handle order toal 

    #order summary
    #delivery date - choice field  base impimentation is from timedelta+2days 


def auto_generate_unique_field_id(sender,instance,created,*args,**kwargs):
    if created:
        # pk makes it impicitely unqiue
        instance.cart_id = random_generator(length=5)+str(instance.pk)
        instance.save()

post_save.connect(auto_generate_unique_field_id,sender=Cart)