from django.contrib.auth.models import BaseUserManager
from . import constants as user_constants

class UserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
       
        if not username:
            raise ValueError('The username must be set')
        #username = self.username
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_doctor', True)
        """extra_fields.setdefault('is_nurse', True)
        extra_fields.setdefault('is_technician', True)"""
        extra_fields.setdefault('user_type',user_constants.SUPERUSER)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(username, password, **extra_fields)