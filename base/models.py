from django.conf import settings
from django.db import models
from django.forms.models import model_to_dict
from django.utils.timezone import now
from.choices import MyChoice as MC
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class BaseModel(models.Model):
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(default=now)

    class Meta:
        abstract = True
    def to_dict(self):
        data = model_to_dict(self)
        data["created_at"] = self.created_at
        data["updated_at"] = self.updated_at
        return data


class AccountManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, first_name, phone, password, **extra_fields):

        values = [email, first_name, phone]

        field_value_map = dict(zip(self.model.REQUIRED_FIELDS, values))

        for field_name, value in field_value_map.items():

            if not value:

                raise ValueError('The {} value must be set'.format(field_name))

        email = self.normalize_email(email)

        user = self.model(

            email=email,

            first_name=first_name,

            phone=phone,

            **extra_fields

        )

        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_user(self, email, first_name, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, first_name, phone, password, **extra_fields)

    def create_superuser(self, email, first_name, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, first_name, phone, password, **extra_fields)

class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=30, null=True)
    phone = models.CharField(max_length=12)
    
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True)
    objects = AccountManager()
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'phone']

    def get_full_name(self):

        return self.first_name

    def get_short_name(self):

        return self.first_name
       