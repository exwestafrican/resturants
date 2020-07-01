from django import forms 

from products.models import ProductVariation,ProductAddon
# PackageContent,

class ProductVariationForm(forms.ModelForm):
    class Meta:
        model = ProductVariation
        fields = ['product_type','price','available','quantity_available']


class ProductAddonForm(forms.ModelForm):

    class Meta:
        model = ProductAddon
        fields = ['add_on_item','product_type','quantity']