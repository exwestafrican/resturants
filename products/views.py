from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import filters
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.settings import api_settings

from products.models import  ProductVariation,Product,Category,AddonItem
# ,PackageContent,Package
from products.serializers import (
                            ProductVariationSerializer,ProductSerializer,AddonItemSerializer,
                            # PackageSerializer,PackageContentSerializer,
                            CategorySerializer)


from products.permissions import IsAdminOrReadOnly
# Create your views here.


class ProductList(APIView):
    
    """
    returns a list of products, variation and necessary
    details atributed to it.
    i.e name :smoothie. variation: small,large, premium
    enables creation of both product and product variation
    by admin user
    """
    queryset                = Product.objects.all()
    serializer_class        = ProductSerializer
    
    #add filters
    permission_classes = [IsAdminOrReadOnly]
    filter_backends    = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields   = ['name','category','product_variation__price']
    search_fields      = ['name','product_variation__price','category__id']


    def get(self,request,format=None):
        self.request.session.set_test_cookie() 
        #set sessionId so user can add item to cart. 
        # check if it worked when user tries to add item to cart
        products = Product.objects.all()
        serializer = ProductSerializer(products,many=True,context={'request': request})
        return Response(serializer.data)

    def post(self,request,format=None):
        """
        handles creation of product + one variation
        creates a diction for variation parameter
        """
        variation_creation_data={
            #data needed to create a product variation
            'product_type':request.data.get('product_type'),
            'price': request.data.get('price'),
            'available':request.data.get('available'),
            'quantity_available':request.data.get('quantity_available')
        }

        #validation stage ignores unnecessary data in request.data
        product_serializer    = ProductSerializer(data=request.data,context={'request': request})
        

        if product_serializer.is_valid():
                #handle product stuff 
                product_serializer.save()
                variation_creation_data['product']= product_serializer.data.get('id')
                headers = self.get_success_headers(product_serializer.data)     
        else:
            return Response(product_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        #if user doesn't specify a product type, create just a product.
        if variation_creation_data['product_type']== None: return Response(product_serializer.data,status=status.HTTP_200_OK,headers=headers)

        variation_serializer  = ProductVariationSerializer(data=variation_creation_data,context={'request': request})

        if variation_serializer.is_valid():
            variation_serializer.save()
        else:
            return Response(variation_serializer.errors,status=status.HTTP_400_BAD_REQUEST)

        return Response(variation_serializer.data,status=status.HTTP_200_OK,headers=headers)
 
    
    def get_success_headers(self, data):
            try:
                return {'Location': str(data[api_settings.URL_FIELD_NAME])}
            except (TypeError, KeyError):
                return {}   
   

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    returns a single product, variation and necessary
    details atributed to it.
    i.e name: smoothie. variation: small,large, premium
    """
    queryset           = Product.objects.all()
    serializer_class   = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]



class ProductVariationListCreate(generics.ListCreateAPIView):
    """
    Handles the creation of product variation
    """  
    queryset          = ProductVariation.objects.all()
    serializer_class  = ProductVariationSerializer
    #permission_classes = [IsAdminUser]

    #allow user add an addon to this?


class ProductVariationDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    returns a single product type or variant
    i.e Basic smoothie. View also allows admin or staff 
    update or delete product.
    """
  
    queryset           = ProductVariation.objects.all()
    serializer_class   = ProductVariationSerializer
    permission_classes = [IsAdminOrReadOnly]
    read_only_fields   = ['product']


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

 




#add creating food item-see all food items 

class AddonItemList(generics.ListCreateAPIView):
    queryset           = AddonItem.objects.all()
    serializer_class   = AddonItemSerializer



class AddonItemDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field       = 'name'
    queryset           = AddonItem.objects.all()
    serializer_class   = AddonItemSerializer



















# class PackageList(generics.ListCreateAPIView):
#     """
#     allows admin users create a new package,
#     list out avaialble package to any user.
#     """
#     queryset           = Package.objects.all()
#     serializer_class   = PackageSerializer
#     permission_classes = [IsAdminOrReadOnly]

# class PackageDetail(generics.RetrieveUpdateDestroyAPIView):
#     """
#     allows admin users edit detail of a specif package,
#     and any user see detail of a specif package
#     """
#     lookup_field       = 'slug'
#     queryset           = Package.objects.all()
#     serializer_class   = PackageSerializer
#     permission_classes = [IsAdminOrReadOnly]





# class CreatePackageContent(generics.CreateAPIView):
#     """
#     allows admin users create a package
#     """
#     queryset            = PackageContent.objects.all()
#     serializer_class    = PackageContentSerializer


# class PackageContentDetail(generics.RetrieveUpdateDestroyAPIView):
#     """
#     provides explicit details about a package content
#     allows admin users,edit and delete content

#     """
#     queryset            = PackageContent.objects.all()
#     serializer_class    = PackageContentSerializer
#     permission_classes  = [IsAdminOrReadOnly]
