from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, username, full_name, phone, email, password=None, **extra_fields):
        if not username:
            raise ValueError('Username is required')
        user = self.model(username=username, full_name=full_name, phone=phone, email=email,
                          is_staff=True, is_superuser=True, **extra_fields)
        user.set_password(password)
        user.save(using=self._db, **extra_fields)
        return user

    def create_superuser(self, username, full_name, phone, email, password=None, **extra_fields):
        return self.create_user(username, full_name, phone, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=False, blank=False)
    username = models.CharField(max_length=255, unique=True, null=False, blank=False)
    full_name = models.CharField(max_length=255, null=False, blank=False)
    is_staff = models.BooleanField(default=False)
    is_female = models.BooleanField(default=False)
    birthday = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=10, null=False, blank=False)
    avatar = models.ImageField(upload_to='uploads/%Y/%m/%d/', null=True, blank=True)
    address = models.CharField(max_length=500)
    is_banned = models.BooleanField(default=False)
    balance = models.FloatField(default=0)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['full_name', 'phone', 'email']

    def __str__(self):
        return self.username

