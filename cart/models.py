# django dependences
from django.contrib.auth import get_user_model, settings
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.db import models
from django.db.models.signals import pre_save, post_save, post_delete, m2m_changed
from django.shortcuts import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

# relative
from products.models import ProductVariation
from products.utils import random_generator

from cart.managers import CartItemManager, CartManager


# Create your models here.


User = settings.AUTH_USER_MODEL

CART_STATUS = [
    ("shopping", "SHOPPING"),
    ("checkout", "CHECKOUT"),
    ("paid", "PAID"),
    ("cancelled", "CANCELLED"),
]


class CartItem(models.Model):
    cart = models.ForeignKey(
        "Cart", related_name="cart_items", on_delete=models.CASCADE
    )
    product = models.ForeignKey(ProductVariation, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    # owner       = models.ForeignKey(User,on_delete=models.CASCADE,blank=True)  #not required ?
    created = models.DateTimeField(auto_now_add=True)
    anonymous_cart_id = models.CharField(max_length=200, blank=True, null=True)
    objects = CartItemManager()

    class Meta:
        # unique together cart and product
        unique_together = ["cart", "product"]

    def clean(self):
        # check to see if quantity available is less than order
        if self.quantity > self.product.quantity_available:
            raise ValidationError(
                {"quantity": _("Order exceeds amount available for sale")}
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} units of {self.product}"

    @property
    def item_total(self):
        return self.product.current_price * self.quantity

    @property
    def product_name(self):
        return self.product.product_name

    @property
    def product_type(self):
        return self.product.type_of_product

    @property
    def product_price(self):
        return self.product.current_price

    def update_cart_total(self):
        cart = self.cart
        # cart.cart_items.all() returns a query set of all items in cart.
        item_total = [item.item_total for item in cart.cart_items.all()]
        cart.total = sum(item_total)
        cart.save()

    @property
    def get_cart_id(self):
        return self.cart.cart_id

    def get_absolute_url(self):
        """
        returns an absolute url path to product
        """
        return reverse("cart-item-detail", kwargs={"pk": self.pk})


def add_to_cart_total(sender, instance, created, *args, **kwargs):
    new_cart_total = instance.update_cart_total()
    if created or instance.cart.total != new_cart_total:
        # if new item was created or exiting item was edited,
        # cart was already updated
        # this is done to avoide recalling an update and also avoids infinite loops
        return new_cart_total


def subtract_from_cart_total(sender, instance, *args, **kwargs):
    instance.update_cart_total()


post_save.connect(add_to_cart_total, sender=CartItem)
post_delete.connect(subtract_from_cart_total, sender=CartItem)


class Cart(models.Model):
    """
   handles updating 
    total cart cost and attributing it to owner
    """

    cart_id = models.CharField(max_length=200, blank=True, unique=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    created = models.DateTimeField(auto_now_add=True, null=True)
    session_id = models.CharField(max_length=200, blank=True, null=True)
    active = models.BooleanField(default=True)  # keep false till payment is paid
    cart_status = models.CharField(
        max_length=200, default="shopping", choices=CART_STATUS
    )

    # updated

    objects = CartManager()

    def __str__(self):
        return str(self.cart_id)

    class Meta:
        ordering = ["-created"]

    def is_cart_anonymous(self):
        return bool(self.owner)

    # define a method tu update cart starus

    # use a many to many signal to handle order toal

    # order summary
    # delivery date - choice field  base impimentation is from timedelta+2days


def auto_generate_unique_field_id(sender, instance, created, *args, **kwargs):
    if created:
        # pk makes it impicitely unqiue
        instance.cart_id = random_generator(length=5) + str(instance.pk)
        instance.save()


post_save.connect(auto_generate_unique_field_id, sender=Cart)


# add signal for if an item is removed from cart
