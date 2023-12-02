from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,PermissionsMixin


class UserManager(BaseUserManager):
    use_in_migrations=True

    def create_user(self,email,password=None,**extra_fields):
        if not email:
            raise ValueError('email is required')
        
        user=self.model(email=self.normalize_email(email),**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,password,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_admin',True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('superuser must have is_staff=true')
        if extra_fields.get('is_admin') is not True:
            raise ValueError('superuser must have is_admin=true')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('superuser must have is_superuser=true')
        
        return self.create_user(email,password,**extra_fields)
    

class CustomUser(AbstractBaseUser,PermissionsMixin):
    username=None
    name=None

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    firstname=models.CharField(max_length=100,null=True)
    lastname=models.CharField(max_length=100,null=True)
    email=models.EmailField(max_length=100,unique=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    mobilenumber=models.CharField(max_length=10,unique=True ,null=True)

    datejoined=models.DateTimeField(auto_now_add=True)
    address=models.CharField(max_length=250,null=True)
    pincode=models.CharField(max_length=10,null=True)
    city=models.CharField(max_length=100,null=True)
    state=models.CharField(max_length=100,null=True)

    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    is_admin=models.BooleanField(default=False)

    objects=UserManager()

    USERNAME_FIELD='email'
       

    def __str__(self):
        if self.name:
            return self.name
        else:
            return self.email