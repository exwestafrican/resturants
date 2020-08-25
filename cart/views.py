from django.shortcuts import render
from django.db.models import Q
from django.db.models.query import QuerySet
from django.http.request import QueryDict

from cart.serializers import CartSerializer, CartItemSerializer
from cart.models import Cart, CartItem
from cart.mixins import CreateCartMixin

from rest_framework import generics, status
from rest_framework.response import Response


# Create your views here.


class CartList(generics.ListAPIView):
    serializer_class = CartSerializer

    def get_queryset(self):
        # if user is authenticated and no anonymous id is provided
        anonymous_cart_id = self.request.query_params.get("anonymous_cart_id", None)
        if self.request.user.is_authenticated and anonymous_cart_id is None:
            cart = Cart.objects.get_users_cart(user=self.request.user)
        elif anonymous_cart_id:
            cart = Cart.objects.get_anonymous_cart(anonymous_cart_id)
        else:
            cart = 0

        return cart

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if len(queryset) == 0:
            return Response(
                data={
                    "message": "please supply an anonymous cart id or autheticated user with a valid cart"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CreateEmptyCart(generics.CreateAPIView):
    serializer_class = CartSerializer


class AddItemsToCart(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    queryset = CartItem.objects.all()

    def create(self, request, *args, **kwargs):
        """
        requires user to pass in anonymous_cart_id gotten from create empty cart.
        anonymout_cart_id must be a valid cart_id
        user requiered to pass in product and quantity 
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if request.user.is_authenticated:
            serializer.save(owner=request.user)
        else:
            serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


# cart item detail

