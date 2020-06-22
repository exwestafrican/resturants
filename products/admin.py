from django.contrib import admin
from products.models import (Package,PackageContent,
                            Product,ProductVariation,
                            ProductImage,
                            Category)

from products.forms import PackageContentForm,ProductVariationForm
# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ['slug']

class ProductVariationInline(admin.TabularInline):
    model = ProductVariation
    form  = ProductVariationForm
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductVariationInline]
    readonly_fields = ['slug']
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name',)
    ordering = ('name',)
    list_per_page = 15
   

class ProductVariationAdmin(admin.ModelAdmin):
    readonly_fields = ['slug']
    list_display = ('slug','current_price','product_name','available')
    list_filter  =('product','available')
    search_fields = ('product','slug')
    list_per_page = 15

class PackageContentFormInline(admin.TabularInline):
    model = PackageContent
    form  = PackageContentForm
    extra = 1
    raw_id_fields = ["product"]

class PackageContentAdmin(admin.ModelAdmin):
    list_display  =('product','package')


class PackageAdmin(admin.ModelAdmin):
    inlines = [PackageContentFormInline]
    list_display  =('name','current_price','available')
    readonly_fields = ['slug']
    list_per_page = 15
    class Meta:
        model = Package


admin.site.register(Product,ProductAdmin)
admin.site.register(PackageContent,PackageContentAdmin)
admin.site.register(ProductVariation,ProductVariationAdmin)
admin.site.register(Package,PackageAdmin)
admin.site.register(ProductImage)
admin.site.register(Category,CategoryAdmin)
