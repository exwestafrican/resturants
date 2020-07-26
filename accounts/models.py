from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import ugettext_lazy as _

from accounts.managers import UserManager



class User(AbstractBaseUser,PermissionsMixin):
    """
    User class inherits from the abstractbaseUser class 
    implementing a fully featured User model with dmin-compliant 
    permissions.identical to django's AbstractUserclass. 
    Email and password are required. Other fields are optional.
    password and password behaviour inherted from AbstractBaseUser
    """
    phone_number  =  PhoneNumberField(
                        unique=True,
                        help_text='phone numbers need to come with extentions, e.g +23481690....',
                        blank=True,null=True)

    email         = models.EmailField(unique=True, max_length=200)
    first_name    = models.CharField(max_length=30, blank=True,null=True)
    last_name     = models.CharField(max_length=30, blank=True, null=True)
    date_joined   = models.DateTimeField(auto_now_add=True)
    is_staff      = models.BooleanField(
                       'staff status',
                        default=False,
                        help_text='Designates whether the user can log into this admin site.',)

    is_active     = models.BooleanField(
                        'active',
                        default=True,
                        help_text='Designates whether this user should be treated as active. '
                                   'Unselect this instead of deleting accounts.',)

    avatar         = models.ImageField(upload_to='avatars/', null=True, blank=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def __str__(self):
        #decided what to call user 
        name = self.email if self.get_short_name() is None else self.get_short_name()
        return name

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '{} {}'.format(self.first_name, self.last_name)
        return full_name.strip() #removes leading and trailing whitespace

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


    @property
    def user_id(self):
        return id

class UserInfo(models.Model):
    pass


# class Address(models.Model):
#     line1         = models.CharField(max_length=150)
#     line2         = models.CharField(max_length=150)
#     postalcode    = models.CharField(max_length=10)
#     city          = models.CharField(max_length=150)
#     country       = models.CharField(max_length=150)