from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator,UniqueValidator

from accounts.custom_serializers import DynamicFieldsModelSerializer
from cart.models import CartItem,Cart
from products.models import ProductVariation
class CartItemSerializer(DynamicFieldsModelSerializer):
   
   
    class Meta:
        model = CartItem
        fields = ['cart','product',
                    'product_name','product_type',
                    'product_price','quantity','item_total']
        read_only_fields = ['cart','product_available']

    

    def get_product_available_for_sale(self,product_variation,*args,**kwargs):
        return product_variation.quantity_available
       
        

    def create(self,validated_data):
            #check if product in cart before creating
            if CartItem.objects.filter( cart=validated_data.get('cart'),
                                        product=validated_data.get('product')
                                        ).exists():
                 raise serializers.ValidationError("You already added this item to cart") 
            else:
                cart_item = CartItem.objects.create(**validated_data)
                return cart_item


    def validate(self,data):
        product_variation = data.get('product')
       
 
        #product being sent is --> product_variation
        if data.get('quantity',1) >  product_variation.quantity_available:
            raise serializers.ValidationError("You've exceeded the amount available for sale") 
        return data
    
    

class CartSerializer(DynamicFieldsModelSerializer):
    cart_items = CartItemSerializer(many=True,fields=[
                        'product_name','product_type',
                        'product_price','quantity','item_total',],read_only=True)
   
    class Meta:
        model = Cart
        fields = ['cart_id','owner','total','session_id','cart_items','active']
        read_only_fields = ['cart_id','owner','total','session_id','active']
        
        #cart_id and owner are implicitely always going to be unique. cart_id: unique = True
        #cart_id and session_id are explictly always going to be unique. cart_id: unique = True, session_id: unique = True

    def create(self,validated_data):
        cart = Cart.objects.create(**validated_data)
        return cart

    