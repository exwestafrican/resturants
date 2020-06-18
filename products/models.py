from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.utils import timezone


from products.utils import image_path,slug_generator,product_variation_slug_generator
from django.utils.text import slugify
# Create your models here.


class ProductQuerySet(models.query.QuerySet):
	def active(self):
		return self.filter(active=True)

class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)


    def create_product(self,**field_name):
        """
        handles how a new product instance should be created
        creates a new product variation instance with default 
        value. 
        """
     
       
        name              = field_name.pop('name')
        slug              = field_name.pop('slug') if 'slug' in field_name.keys() else slugify(name) 
        product_type      = field_name.pop('product_type') if 'product_type' in field_name.keys() else 'Basic'
        product           = Product.objects.create(name=name,slug=slug,**field_name)
      
        #allow users create variation from here 
        # product_variation = ProductVariation.objects.create(product=product,product_type=product_type,price=price)
        return product



class Product(models.Model):
    """
    Descripes everything about a product 
    """
    name                = models.CharField(max_length=200,unique=True)
    description         = models.TextField(blank=True, null=True)
    slug                = models.SlugField(unique=True,blank=True)
    category            = models.ForeignKey('Category',on_delete=models.CASCADE)
    created             = models.DateTimeField(default=timezone.localtime(),blank=True)

    objects = ProductManager()
    

    class Meta:
        ordering = ['-name']
        # verbose_name_plural = _('Product Description')

    def __str__(self):
        return self.name
        
    @property
    def product_image(self):
        """
        gets all images associated with
        instance (product)
        """
        return ProductImage.objects.filter(product=self)

    @property
    def product_categroy(self):
        return self.category.name


post_save.connect(slug_generator,sender=Product)



class ProductImage(models.Model):
    """
    Assigns images to a product 
    """
    product             = models.ForeignKey('Product',on_delete=models.CASCADE)
    image               = models.ImageField(upload_to=image_path,unique=True,null=True,blank=True)  #adds an extra layer of security
    
   
    def __str__(self):
        return self.product.slug

class ProductVariationQuerySet(models.query.QuerySet):
	def active(self):
		return self.filter(available=True)

class ProductVariationManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

class ProductVariation(models.Model):
    """
    Stores single products as well as variations
    variations attributed to a single product
    """
    product             = models.ForeignKey('Product',related_name='product_variation',on_delete=models.CASCADE,null=True)
    product_type        = models.CharField(
                            _('type'),
                            max_length=200,
                            default='Basic',
                            help_text='this could be a different colour, size,or more things out of the box')
    description         = models.TextField(blank=True, null=True)
    price               = models.DecimalField(decimal_places=2,max_digits=7)
    sale_price          = models.DecimalField(decimal_places=2, max_digits=7, null=True, blank=True)
    slug                = models.SlugField(unique=True,blank=True,null=True) #make this read only in admin
    available           = models.BooleanField(default=True)
    quantity_available  = models.PositiveIntegerField(null=True,blank=True,default=None)
    created             = models.DateTimeField(auto_now_add=True)
    objects             = ProductVariationManager()

    class Meta:
        verbose_name=_('Product Variation')
        verbose_name_plural= _('Product Variation')
        unique_together = ['product', 'product_type']

    def __str__(self):
        return str(self.slug)

    @property
    def product_name(self):
        return str(self.product.name)

    @property
    def current_price(self):
        if self.sale_price is not None:return self.sale_price
        return self.price
    
    @property
    def product_slug(self):
        """ method present for better naming convention"""
        return self.slug

post_save.connect(product_variation_slug_generator,sender=ProductVariation)
	

class Category(models.Model):
    name            = models.CharField(max_length=200,unique=True)
    slug            = models.SlugField(unique=True,null=True,blank=True)
    description     = models.TextField(null=True,blank=True)
    created         = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


    def __str__(self):
        return self.name

    

post_save.connect(slug_generator,sender=Category)
