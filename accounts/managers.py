from django.contrib.auth.base_user import BaseUserManager
from django.contrib import auth


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password,phone_number, **extra_fields):
        """
        Create and save a user with the given email, and password.
        and optional phone number
        """
        if not email:
            raise ValueError('You need to provide an Email')
        email = self.normalize_email(email)
        user  = self.model(email=email,phone_number=phone_number,**extra_fields)
        
        #ask for phone number?
        user.set_password(password)
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, email):
        """ 
        authentication method runs this to
        run a get call on accounts.User.objects
        which is the now default User model.
        """
        return self.get(**{self.model.USERNAME_FIELD: email})


    def create_user(self, email=None,password=None,phone_number=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email,password,phone_number, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

    def with_perm(self, perm, is_active=True, include_superusers=True, backend=None, obj=None):
        if backend is None:
            backends = auth._get_backends(return_tuples=True)
            if len(backends) == 1:
                backend, _ = backends[0]
            else:
                raise ValueError(
                    'You have multiple authentication backends configured and '
                    'therefore must provide the `backend` argument.'
                )
        elif not isinstance(backend, str):
            raise TypeError(
                'backend must be a dotted import path string (got %r).'
                % backend
            )
        else:
            backend = auth.load_backend(backend)
        if hasattr(backend, 'with_perm'):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        return self.none()

