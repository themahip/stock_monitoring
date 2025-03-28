from django.contrib.auth.hashers import check_password, make_password
from django.db import models
from django.contrib.auth.models import AbstractUser

from shared.helpers.logging_helper import logger
from .base import UserBaseModel


class User(UserBaseModel,AbstractUser):
    username= models.CharField(unique=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.email
    
    def setpassword (self, raw_password):
        """set user password with proper hashing"""
        self.password= make_password(raw_password)
        logger.info(f"Password set for {self.username}")


    def create_user(self, username, email, name):
        """Create and save a new user"""
        self.username= username
        self.email= email
        self.name= name
        self.save()
        logger.info(f"user created: {self.username}")
    
    def authenticate_user(self, password):
        """verify user identity"""
        is_valid= check_password(password, self.password)
        if is_valid:
            logger.info(f"Authentication successfull for  {self.username}")
            return True
        else:
            logger.info(f"Authentication failed for {self.username}. Wrong password")
            return False