
from rest_framework import serializers
from rest_framework.reverse import reverse
from rest_framework.validators import UniqueTogetherValidator,UniqueValidator

from django.utils.text import slugify

from products.models import (Product,ProductVariation,
                             ProductImage,ProductAddon,
                             AddonItem,Category,
                            # Package,PackageContent,
                            )


from accounts.custom_serializers import (DynamicFieldsHyperlinkedModelSerializer,
                                         DynamicFieldsModelSerializer)




class ProductImageSerializer(DynamicFieldsHyperlinkedModelSerializer):
  
    class Meta:
        model = ProductImage
        fields=['id','url','image','product']


class AddonItemSerializer(DynamicFieldsModelSerializer):
    url                = serializers.SerializerMethodField()
    class Meta:
        model = AddonItem
        fields = ['name','quantity_available','available','url']

class ProductAddonSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = ProductAddon
        fields = ['add_on_item_name','type_of_product','quantity']      


class ProductVariationSerializer(DynamicFieldsModelSerializer):
    product_image      = ProductImageSerializer(many=True,fields=['url'],read_only=True)
    url                = serializers.SerializerMethodField()
    content            = ProductAddonSerializer(many=True,fields=['add_on_item_name','quantity'],read_only=True)

   

    class Meta:
        model  = ProductVariation
        fields = [  'id','url','product_name','product',
                    'product_image','product_type','content',
                    'price',
                    'product_slug', 'sale_price','current_price',
                    'description','available','quantity_available']
                
        validators = [
            UniqueTogetherValidator(
                queryset=ProductVariation.objects.all(),
                fields=['product', 'product_type']
            )
        ]
       

        read_only_fields = []


    def get_url(self,obj):
        """
        takes the absolute url of a view, 
        and appends a full path to it
        absolute_url = product/<int:pk>
        full path = https://<domain_name>/<absolute_url>
        """
        return self.context['request'].build_absolute_uri(obj.get_absolute_url())
           




class ProductSerializer(DynamicFieldsHyperlinkedModelSerializer):
    product_variation  = ProductVariationSerializer(many=True,read_only=True,
                        fields=['id','url','product_image','content',
                                 'current_price','description','product_type','available','variation_add_ons'])
   
    category           = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
   
    
    name               = serializers.CharField(max_length=200,
                            validators = [ UniqueValidator( 
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


          
     


























# class PackageContentSerializer(DynamicFieldsModelSerializer):
#     url = serializers.SerializerMethodField()
#     class Meta:
#         model = PackageContent
#         fields = ['package','url','product','product_name','quantity']

#         validators = [
#             UniqueTogetherValidator(
#                 queryset=PackageContent.objects.all(),
#                 fields=['package', 'product'],
#                 message = "this product already exists in package, you can update it's qty on a different view or change the product"
#             )
#         ]

#     def get_url(self,obj):
#         """
#         takes the absolute url of a view, 
#         and appends a full path to it
#         """
#         return self.context['request'].build_absolute_uri(obj.get_absolute_url())


# class PackageSerializer(DynamicFieldsModelSerializer):
#     package_content = PackageContentSerializer(many=True,read_only=True,fields=['product_name','quantity','url'])
#     url            = serializers.SerializerMethodField()
#     class Meta:
#         model = Package
#         fields  = ['id','name','url','available','package_content','price','sale_price','current_price','available','slug']
#         read_only_fields = ['slug']

#     def get_url(self,obj):
#         return self.context['request'].build_absolute_uri(obj.get_absolute_url())

   






