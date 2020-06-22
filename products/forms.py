from django import forms 

from products.models import PackageContent,ProductVariation


class ProductVariationForm(forms.ModelForm):
    class Meta:
        model = ProductVariation
        fields = ['product_type','price','available','quantity_available']

class PackageContentForm(forms.ModelForm):

    class Meta:
        model = PackageContent
        fields = ['package','product','quantity']