from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.utils import timezone
from django.shortcuts import reverse
    


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
        product_type      = field_name.pop('product_type') if 'product_type' in field_name.keys() else 'regular'
        product           = Product.objects.create(name=name,slug=slug,**field_name)
      
        #allow users create variation from here 
        # product_variation = ProductVariation.objects.create(product=product,product_type=product_type,price=price)
        return product



class Product(models.Model):
    """
    Descripes everything 
    about a product 
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
    def product_categroy(self):
        return self.category.name


post_save.connect(slug_generator,sender=Product)



class ProductImage(models.Model):
    """
    Assigns images to a product 
    """
    product             = models.ForeignKey('ProductVariation',on_delete=models.CASCADE)
    image               = models.ImageField(upload_to=image_path,unique=True,null=True,blank=True)  #adds an extra layer of certaintiy
    
   
    def __str__(self):
        return str(self.product)



class ProductVariationQuerySet(models.query.QuerySet):
	def active(self):
		return self.filter(available=True)

class ProductVariationManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)


class ProductVariation(models.Model):
    """
    Stores single products as well as variations. 
    Variations attributed to a single product
    """
    product             = models.ForeignKey('Product',related_name='product_variation',on_delete=models.CASCADE,null=True)
    product_type        = models.CharField(
                            _('type'),
                            max_length=200,
                            blank=True,
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
        #formarly self.slug
        return f'{self.product_name} ({self.type_of_product})'

    @property
    def product_name(self):
        return str(self.product.name)

    @property
    def product_variation_name(self):
        return f'{self.product_name} ({self.type_of_product})'

    @property
    def type_of_product(self):
        return str(self.product_type)

    @property
    def current_price(self):
        """
        decides current price of product picks sales price if available,
        else displays actual product price.
        """
        current_price = self.sale_price if self.sale_price is not None else self.price
        return current_price
    
    @property
    def product_slug(self):
        """ 
        method present for better naming convention.
        """
        return self.slug

    def slugify_product_name(self):
        """
        returns the slug representation of product name. 
        """
        return slugify(self.product_name)

    @property
    def product_image(self):
        """
        gets all images associated with instance (product)
        """
        return ProductImage.objects.filter(product=self)


    def get_absolute_url(self):
        """
        returns an absolute url path to product
        """
        kwargs={
                'product_name':slugify(self.slugify_product_name()),
                 'pk' :self.pk
                }
        return reverse('productvariation-detail', kwargs=kwargs)

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


class AddonItem(models.Model):
    """

    """
    name                  = models.CharField(max_length=200,unique=True)
    quantity_available    = models.PositiveIntegerField(default=1)
    available             = models.BooleanField(default=True)
    created               = models.DateTimeField(default=timezone.localtime(),blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product-addons-detail', kwargs={'name':slugify(self.name)})

class ProductAddon(models.Model):
    """
    this adds products to package
    """
    add_on_item          = models.ForeignKey('AddonItem',on_delete=models.CASCADE,null=True)
    product_type         = models.ForeignKey('ProductVariation',related_name='content', on_delete=models.CASCADE)
    quantity             = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = _('Addon')
        verbose_name_plural = _('Addons')
        constraints = [
                models.UniqueConstraint(fields=['product_type', 'add_on_item'], name='unique_combination')
        ]

    @property
    def add_on_item_name(self):
        return self.add_on_item.name  

    @property
    def type_of_product(self):
        return self.product_type.type_of_product


























class PackageQuerySet(models.query.QuerySet):
	def active(self):
		return self.filter(available=True)

class PackageManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)
    

class Package(models.Model):
    """
    this model 
    create a new package
    and gives specific details related to package
    """
    name        = models.CharField(max_length=200,unique=True)
    price       = models.DecimalField(decimal_places=2,max_digits=7)
    description = models.TextField(blank=True, null=True)
    slug        = models.SlugField(unique=True,blank=True) 
    sale_price  = models.DecimalField(decimal_places=2, max_digits=7, null=True, blank=True)
    available   = models.BooleanField(default=True)
    created     = models.DateTimeField(auto_now_add=True)
    objects     = PackageManager()

    #add package content as inline admin

    def __str__(self):
        return str(self.name)
        
    @property
    def current_price(self):
        """
        decides current price of product
        picks sales price if available,
        else displays actual product price.
        """
        current_price = self.sale_price if self.sale_price is not None else self.price
        return current_price

    def get_absolute_url(self):
        """
        returns an absolute url path to product
        """
        
        return reverse('package-detail', kwargs={'slug' :self.slug})

post_save.connect(slug_generator,sender=Package)


#create product variation addon 
class PackageContent(models.Model):
    """
    this adds products to package
    """
    package         = models.ForeignKey('Package',related_name='package_content', on_delete=models.CASCADE)
    product         = models.ForeignKey('Product',on_delete=models.CASCADE)
    # product_type    = models.ForeignKey('ProductVariation',on_delete=models.CASCADE) #new
    quantity        = models.PositiveIntegerField()
	
    def __str__(self):
        return str(self.package)

    @property
    def product_name(self):
        """
        returns name of product in package. 
        """
        return str(self.product.name)

  
    class Meta:
        verbose_name = _('Package Content')
        verbose_name_plural = _('Package Content')
        constraints = [
                models.UniqueConstraint(fields=['package', 'product'], name='unique_packaged_product')
        ]
        #unique together, package and product

    def get_absolute_url(self):
        """
        returns an absolute url path to package content
        """
        return reverse('package-content-detail', kwargs={'pk' :self.pk})
    
   
