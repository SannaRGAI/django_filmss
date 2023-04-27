from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import AbstractUser


class CustomUserManager(BaseUserManager):

    def _create(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password, **extra_fields):
        return self._create(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        return self._create(email, password, **extra_fields)

class CustomUser(AbstractBaseUser):
    use_in_migrations = True

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=55, blank=True, null=True)
    last_name = models.CharField(max_length=55, blank=True, null=True)
    username = models.CharField(unique=True, max_length=55)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    def has_module_perms(self, app_label):
        return self.is_staff
    
    def has_perm(self, obj):
        return self.is_staff

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        if self.name:
            return f'{self.name} -> {self.username}'
        else:
            return f'{self.email} -> {self.username}'