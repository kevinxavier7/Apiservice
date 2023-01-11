from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

class UserManager(BaseUserManager):

    def createUser(self, username, password, full_name, email, is_staff, is_superuser, **extra_fields):
        user = self.model(
            username = username,
            full_name = full_name,
            email = email,
            is_staff = is_staff,
            is_superuser = is_superuser,
            **extra_fields
        )

        user.set_password(password)
        user.save(using = self.db)
        return user
    
    def create_user(self, username, password, full_name, email, **extra_fields):
        return self.createUser(username, password, full_name, email, False, False, **extra_fields)

    def create_superuser(self, username, password, full_name, email, **extra_fields):
        return self.createUser(username, password, full_name, email, True, True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length = 100, unique=True)
    full_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True, max_length=100)
    creation_date =models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['full_name', 'email']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return f'{self.full_name}'

