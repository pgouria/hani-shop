from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from .managers import UserManager
from shop.models import Product


class User(AbstractBaseUser):
    email = models.EmailField(max_length=100, unique=True , verbose_name='ایمیل')
    full_name = models.CharField(max_length=100, verbose_name='نام و نام خانوادگی')
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    likes = models.ManyToManyField(Product, blank=True, related_name='likes')
    address = models.CharField(max_length=200, null=True, blank=True , verbose_name='آدرس')
    phone = models.CharField(max_length=200, null=True, blank=True , verbose_name='شماره تلفن')
    
    # set a manager role for shop manager to access orders and products
    is_manager = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']


    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def get_likes_count(self):
        return self.likes.count()
    

