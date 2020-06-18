from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework import filters
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework import generics
from rest_framework.response import Response

from products.models import  ProductVariation,Product,Category
from products.serializers import (
                            ProductVariationSerializer,
                            ProductSerializer,
                            CategorySerializer)


from products.permissions import IsAdminOrReadOnly
# Create your views here.


class ProductList(generics.ListCreateAPIView):
    
    """
    returns a list of products, variation and necessary
    details atributed to it.
    i.e name :smoothie. variation: small,large, premium
    """
    queryset                = Product.objects.all()
    serializer_class        = ProductSerializer
    
    #add filters
    # permission_classes = [IsAdminOrReadOnly]
    filter_backends    = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields   = ['name','category','product_variation__price']
    search_fields      = ['name','product_variation__price','category__id']
    
   
   

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    returns a single product, variation and necessary
    details atributed to it.
    i.e name: smoothie. variation: small,large, premium
    """
    queryset          = Product.objects.all()
    serializer_class  = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]



class ProductVariationCreate(generics.CreateAPIView):
    """
    Handles the creation of product variation
    """  
    queryset          = ProductVariation.objects.all()
    serializer_class  = ProductVariationSerializer
    permission_classes = [IsAdminUser]


class ProductVariationDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    returns a single product type or variant
    i.e Basic smoothie. View also allows admin or staff 
    update or delete product.
    """
    
    queryset          = ProductVariation.objects.all()
    serializer_class  = ProductVariationSerializer
    # permission_classes = [IsAdminOrReadOnly]
    

    read_only_fields = ['product']


    def retrieve(self, request, *args, **kwargs):
        """ 
        method is run by get to retrieve element by
        pk as specified in look_up_url.
        class fields argument is added to kwargs
        to take advange of DynamicFieldsHyperlinkedModelSerializer
        """
       
        instance = self.get_object()
        read_only_fields = self.read_only_fields
        serializer = self.get_serializer(instance,read_only_fields=read_only_fields)
        return Response(serializer.data)

      

class ProductCategoryDetail(generics.RetrieveDestroyAPIView):
    queryset         = Category.objects.all()
    serializer_class = CategorySerializer


class ProductCategoryList(generics.ListCreateAPIView):
    queryset           = Category.objects.all()
    serializer_class   = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

 

