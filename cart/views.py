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


class CartList(generics.ListAPIView, CreateCartMixin):
    serializer_class = CartSerializer

    def get_queryset(self):
        queryset = self.get_cart_queryset()
        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.all()
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_cart_queryset())

        if len(queryset) == 0:
            # users might have zero active cart. anon user might have no cart:None
            return Response(
                data={"message": "You currently have no active cart, please create one"}
            )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


# if cart_id in session_id use that to add item to cart
# else create new cart


class CartItemList(generics.ListCreateAPIView, CreateCartMixin):
    serializer_class = CartItemSerializer
    queryset = CartItem.objects.all()
    model = CartItem

    # only show cart items that belong users

    def get_or_create_cart(self, request, *args, **kwargs):
        cart = self.get_cart_queryset()
        # i can overide the save method.
        if len(cart) == 0:
            cart = self.create_new_cart(request, *args, **kwargs)
        else:
            cart = cart.first()
        return cart

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        cart = self.get_or_create_cart(request, *args, **kwargs)
        if cart is not None:
            serializer.save(cart=cart)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )
        else:
            # if i can't activate cookies on browser throw this error
            # create new error messsage
            serializer.error_messages[
                "cookie_error"
            ] = "You need to enable cookies on this browser or Autheticate yourself to create or add item to a cart"
        return Response(
            serializer.error_messages.get("cookie_error"),
            status=status.HTTP_400_BAD_REQUEST,
        )

#cart item detail