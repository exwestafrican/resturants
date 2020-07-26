from django.shortcuts import render
from django.db.models import Q
from django.db.models.query import QuerySet
from django.http.request import QueryDict

from cart.serializers import CartSerializer,CartItemSerializer
from cart.models import Cart,CartItem
from cart.mixins import CreateCartMixin

from rest_framework import generics,status
from rest_framework.response import Response



# Create your views here.

class CartList(generics.ListCreateAPIView,CreateCartMixin):
    serializer_class    = CartSerializer
    
    def get_queryset(self):
        queryset = self.get_cart_queryset()
        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.all()
        return queryset


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_cart_queryset())

        if len(queryset) == 0:
            #users might have zero active cart. anon user might have no cart:None
            return Response(data={'message':'You currently have no active cart, please create one'})

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        content = self.create_new_cart(request, *args, **kwargs)
        return Response(**content)

    

    


#if cart_id in session_id use that to add item to cart 
#else create new cart 

class CartItemList(generics.ListCreateAPIView,CreateCartMixin):
    serializer_class    = CartItemSerializer
    queryset            = CartItem.objects.all()
    model               = CartItem

    #only show cart items that belong users
    

    

    def get_or_create_cart(self,request,*args,**kwargs):
        cart = self.get_cart_queryset()
        #i can overide the save method. 
        if len(cart) == 0:
            cart = self.create_new_cart(request,*args,**kwargs)
        else:
            cart = cart.first()
        return cart


    def create(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer,request)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        

    def perform_create(self,serializer,request,*args,**kwargs):
        #i can overide the save method. 
        cart = self.get_or_create_cart(request,*args,**kwargs)
        
        serializer.save(cart=cart)


def append_extra_kwargs_to_request_data(request_data,extra_kwargs):
    """
    takes in a dictionary and a Querydict, 
    appends extra_kwargs to querydict and returns a new query_dict
    """
    for key , value in request_data:
        extra_kwargs[key] = value
    data = QueryDict(extra_kwargs)
    print(data)
    return data



 # figure out if user has and active cart
    # if no cart, create a new cart for user
    #if get cart queryset is not None, add item to cart, 
    #esle create cart and add item 
    # def get_queryset(self):
    #     queryset = self.get_cart_queryset()
    #     if isinstance(queryset, QuerySet):
    #         # Ensure queryset is re-evaluated on each request.
    #         queryset = queryset.all()
    #     return queryset
