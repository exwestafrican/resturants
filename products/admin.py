from django.contrib import admin
from products.models import (Package,PackageContent,
                            Product,ProductVariation,ProductAddon,
                            ProductImage,AddonItem,
                            Category,
                            
                            )

from products.forms import ProductVariationForm,ProductAddonForm
# PackageContentForm,
# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ['slug']

class ProductVariationInline(admin.TabularInline):
    model = ProductVariation
    form  = ProductVariationForm
    extra = 1

class ProductAddonFormInline(admin.TabularInline):
    model = ProductAddon
    form  = ProductAddonForm
    extra = 1 
    raw_id_fields = ["add_on_item"]

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductVariationInline]
    readonly_fields = ['slug']
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name',)
    ordering = ('name',)
    list_per_page = 15
   

class ProductVariationAdmin(admin.ModelAdmin):
    inlines = [ProductAddonFormInline]
    readonly_fields = ['slug']
    list_display = ('product_name','type_of_product','current_price','available')  #added __str___ : pizza -- large -- 5,000 -- available
    list_filter  =('product','available')
    search_fields = ('product','slug')
    list_per_page = 15


class ProductAddonAdmin(admin.ModelAdmin):
    list_display = ('add_on_item','product_type','quantity')


class AddonItemAdmin(admin.ModelAdmin):
    readonly_fields = ['created']

# class PackageContentFormInline(admin.TabularInline):
#     model = PackageContent
#     # form  = PackageContentForm
#     extra = 1
#     raw_id_fields = ["product"]

# class PackageContentAdmin(admin.ModelAdmin):
#     list_display  =('product','package')


# class PackageAdmin(admin.ModelAdmin):
#     inlines = [PackageContentFormInline]
#     list_display  =('name','current_price','available')
#     readonly_fields = ['slug']
#     list_per_page = 15
#     class Meta:
#         model = Package




admin.site.register(Product,ProductAdmin)
admin.site.register(ProductVariation,ProductVariationAdmin)
admin.site.register(ProductImage)
admin.site.register(AddonItem,AddonItemAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(ProductAddon,ProductAddonAdmin)

# admin.site.register(Package,PackageAdmin)
# admin.site.register(PackageContent,PackageContentAdmin)