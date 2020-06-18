
from rest_framework import serializers
from rest_framework.reverse import reverse
from rest_framework.validators import UniqueTogetherValidator,UniqueValidator

from django.utils.text import slugify

from products.models import (Product,
                            ProductVariation,
                            ProductImage,
                            Category)


from accounts.serializers import DynamicFieldsHyperlinkedModelSerializer


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields`and 'read_only_fields argument that
    controls which fields should be displayed and when some fields should be set as read_only
    """

    def __init__(self,*args,**kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)
      

        read_only_fields = kwargs.pop('read_only_fields',None)
       
        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)
       
       
        if fields is not None:
            
            allowed     = set(fields)
            exisiting   = set(self.fields)
            
            for field_name in exisiting-allowed:
                #remove items from dict like obj
                self.fields.pop(field_name)
    
        if read_only_fields is not None:
           
            try:
                self.Meta.read_only_fields

            except AttributeError:
                raise AttributeError (f"{self.__class__.__name__} does not have an "
                        "attribute read_only_fields, create an empty list in Meta class to resolve this "
                        "Class Meta: read_only_fields=[ ]")

            else:
                #using a set to prevent repetition of fields appended to 
                # read_only_frields due to user refreshing page
                model_read_only_fields = set()
                
                for field in read_only_fields:
                    model_read_only_fields.add(field)
              
                self.Meta.read_only_fields = list(model_read_only_fields)



class ProductImageSerializer(DynamicFieldsHyperlinkedModelSerializer):
    class Meta:
        model = ProductImage
        fields=['id','url','image','product']
       


class ProductVariationSerializer(DynamicFieldsHyperlinkedModelSerializer):
    # product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    product_image      = ProductImageSerializer(many=True,fields=['url'],read_only=True)
    class Meta:
        model = ProductVariation
        fields = [
            'id','url',
            'product','product_name',
            'product_image',
            'product_type','price',
            'product_slug', 'sale_price',
            'current_price','description',
            'available','quantity_available']
           
        validators = [
            UniqueTogetherValidator(
                queryset=ProductVariation.objects.all(),
                fields=['product', 'product_type']
            )
        ]

        read_only_fields = []

    

 

class ProductSerializer(DynamicFieldsHyperlinkedModelSerializer):
    product_variation  = ProductVariationSerializer(many=True,read_only=True,
                        fields=['id','url','product_name','product_image',
                                 'current_price','description','product_type','available'])
   
    category           = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
   

    name               = serializers.CharField(max_length=200,
                            validators = [UniqueValidator( 
                                    queryset=Product.objects.all(), 
                                    message="a product with this name already exists" ) 
                                    ])

    class Meta:
        model = Product
        fields = ['name','id','url','product_categroy','category','description','slug','product_variation']
        extra_kwargs = {
                'slug': {'read_only': True},
        }


    
    def create(self,validated_data):
        """
        handles how product serializer
        creates product instance 
        """
        product = Product.objects.create_product(**validated_data)
        return product

   
    
        
class CategorySerializer(DynamicFieldsHyperlinkedModelSerializer):
    product_set = ProductSerializer(many=True,read_only=True,fields=['name','product_image','url'])
    class Meta:
        model = Category
        fields=['id','url','name','slug','description','product_set']

        read_only_fields = ['slug']
          
     







