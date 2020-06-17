from django.contrib import admin
from products.models import (Product,
                            ProductVariation,
                            ProductImage,
                            Category)

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ['slug']

class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ['slug']

class ProductVariationAdmin(admin.ModelAdmin):
    readonly_fields = ['slug']




admin.site.register(Product,ProductAdmin)
admin.site.register(ProductVariation,ProductVariationAdmin)
admin.site.register(ProductImage)
admin.site.register(Category,CategoryAdmin)
