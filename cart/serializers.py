from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

from accounts.custom_serializers import DynamicFieldsModelSerializer
from cart.models import CartItem, Cart
from products.models import ProductVariation


class CartItemSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = CartItem
        fields = [
            "product",
            "product_name",
            "product_type",
            "product_price",
            "quantity",
            "item_total",
            "anonymous_cart_id",
        ]
        read_only_fields = ["product_available"]

    def get_product_available_for_sale(self, product_variation, *args, **kwargs):
        return product_variation.quantity_available

    def create(self, validated_data):
        # check if anonymous id is valid
        cart = Cart.objects.filter(cart_id=validated_data.get("anonymous_cart_id"))
        if not cart.exists():
            raise serializers.ValidationError("invalid anonymous cart ID")
        cart = cart.first()
        if not cart.active:
            raise serializers.ValidationError(
                "anonymous cart ID is not active,please create a new one"
            )
        # check that cart item is on front end unique.
        cart_item = CartItem.objects.create(cart=cart, **validated_data)
        return cart_item

    def validate(self, data):
        product_variation = data.get("product")

        # product being sent is --> product_variation
        if data.get("quantity", 1) > product_variation.quantity_available:
            raise serializers.ValidationError(
                "You've exceeded the amount available for sale"
            )
        return data


class CartSerializer(DynamicFieldsModelSerializer):
    cart_items = CartItemSerializer(
        many=True,
        fields=[
            "product_name",
            "product_type",
            "product_price",
            "quantity",
            "item_total",
        ],
        read_only=True,
    )

    class Meta:
        model = Cart
        fields = ["cart_id", "owner", "total", "session_id", "cart_items", "active"]
        read_only_fields = ["cart_id", "owner", "total", "session_id", "active"]

        # cart_id and owner are implicitely always going to be unique. cart_id: unique = True
        # cart_id and session_id are explictly always going to be unique. cart_id: unique = True, session_id: unique = True

    def create(self, validated_data):
        cart = Cart.objects.create(**validated_data)
        return cart

