from django.db import models
from products.utils import random_generator
from products.models import Product


class CartItemQuerySet(models.query.QuerySet):
    pass


class CartItemManager(models.Manager):
    def get_queryset(self):
        return CartItemQuerySet(self.model, using=self._db)


class CartQuerySet(models.query.QuerySet):
    def get_users_cart(self, user):
        return self.filter(owner=user, active=True)

    def get_anonymous_cart(self, id):
        return self.filter(cart_id=id, active=True)


class CartManager(models.Manager):
    def get_queryset(self):
        return CartQuerySet(self.model, using=self._db)

    def create(self, **field_name):
        new_cart = self.model(**field_name)
        new_cart.save()
        return new_cart

    def get_users_cart(self, user):
        return self.get_queryset().get_users_cart(user)

    def get_anonymous_cart(self, id):
        return self.get_queryset().get_anonymous_cart(id)

