from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator,UniqueValidator

from accounts.custom_serializers import DynamicFieldsModelSerializer
from cart.models import CartItem,Cart
from products.models import ProductVariation
class CartItemSerializer(DynamicFieldsModelSerializer):
    # product               = serializers.PrimaryKeyRelatedField(max_length=200,
    #                         validators = [ UniqueValidator( 
    #                                 queryset=CartItem.objects.all(), 
    #                                 message="you already added this to cart" ) 
    #                                 ])
   
    class Meta:
        model = CartItem
        fields = ['cart','product','product_name','product_price','quantity','item_total']
        read_only_fields = ['cart','product_available']

    

    def get_product_available_for_sale(self,product,*args,**kwargs):
        cart_item = CartItem.objects.filter(product=product).first()
        return cart_item.product_available()
        

    def create(self,validated_data):
            cart_item = CartItem.objects.create(**validated_data)
            return cart_item

    def validate(self,data):
        product = data.get('product')
        cart = data
       
        if data['quantity'] > self.get_product_available_for_sale(product=product) :
            raise serializers.ValidationError("You've exceeded the amount available for sale") 
        return data

class CartSerializer(DynamicFieldsModelSerializer):
    cart_items = CartItemSerializer(many=True,fields=['product_name','product_price','quantity','item_total',],read_only=True)
   
    class Meta:
        model = Cart
        fields = ['cart_id','owner','total','session_id','cart_items','active']
        read_only_fields = ['cart_id','owner','total','session_id','active']
        
        #cart_id and owner are implicitely always going to be unique. cart_id: unique = True
        #cart_id and session_id are explictly always going to be unique. cart_id: unique = True, session_id: unique = True

    def create(self,validated_data):
        cart = Cart.objects.create(**validated_data)
        return cart

    