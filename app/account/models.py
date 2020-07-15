from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class UserManager(BaseUserManager):

    def create_user(self, email, password, account_type, *args, **kwargs):
        if not email:
            raise ValueError('Email field is compulsory')
        if not account_type:
            raise ValueError('Account type is compulsory')
        email = self.normalize_email(email)
        user = self.model(email=email, account_type=account_type, *args, **kwargs)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, null=False, unique=True)
    password = models.CharField(max_length=255)
    account_type = models.CharField(max_length=20)

    objects = UserManager()

    USERNAME_FIELD = 'email'
