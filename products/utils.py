import os
import random
import string

from django.utils.text import slugify

def random_generator(length=3):
   random_stuff = [random.choice(string.ascii_lowercase+string.digits) for _ in range(length)]
   return ''.join(random_stuff)


def make_filename(filename):
    """ takes a file name and renames it using random char"""
    name,ext = os.path.splitext(filename)
    name = 'sur'+random_generator()
    new_filename = f'{name}{ext}'
    return new_filename


def image_path(instance,filename):
    """ creates a new file path and verifies uniqueness"""
    klass = instance.__class__
    klass_name = instance.__class__.__name__.lower()
 

    renamed_file = make_filename(filename)
    upload_path = f'{klass_name}/{instance}/{renamed_file}'
    queryset = klass.objects.filter(image__iexact=upload_path)

    while queryset.exists():
        #check if upload path exist for product and create a new one if true
        renamed_file = make_filename(filename)
        upload_path = f'{klass_name}/{instance}/{renamed_file}'
        queryset = klass.objects.get(image__iexact=upload_path)

    return upload_path



def slug_generator(sender,instance,created,*args,**kwargs):
    """
    generates slug from name attribute
    when models is first created
    or title is changed
    """

    if created or slugify(instance.name)!= instance.slug:
        instance.slug = slugify(instance.name)
        instance.save()
   

def product_variation_slug_generator(sender,instance,created,*args,**kwargs):
    """
    generates slug from product and 
    product type attribute
    when models is first created
    or attributes change
    """
    slug = slugify(f'{instance.product.name}-{instance.product_type}')
    if created or slug != instance.slug:
        instance.slug = slug
        instance.save()



