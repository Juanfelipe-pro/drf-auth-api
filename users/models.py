from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)
from django.contrib.auth.hashers import make_password

from roles.models import Role

# Create your models here.
class CustomUserManager(BaseUserManager):                       
    def create_user(self, email, password=None, **extra_fields):
        if not email:                                          
            raise ValueError("El usuario debe tener un email válido")
        email = self.normalize_email(email)                    
        user = self.model(email=email, **extra_fields)         
        user.password = make_password(password)                
        user.save(using=self._db)                              
        return user                                            

    def create_superuser(self, email, password=None, **extra_fields): 
        extra_fields.setdefault("is_staff", True)              
        extra_fields.setdefault("is_superuser", True)          
        return self.create_user(email, password, **extra_fields)
    

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)                    
    first_name = models.CharField(max_length=30, blank=True)   
    last_name = models.CharField(max_length=30, blank=True)    
    is_active = models.BooleanField(default=True)              
    is_staff = models.BooleanField(default=False)              
    role = models.ForeignKey(                                  
        Role, on_delete=models.SET_NULL, null=True, blank=True, related_name="users"
    )

    objects = CustomUserManager()                             

    USERNAME_FIELD = "email"                                   
    REQUIRED_FIELDS = []                                       

    def __str__(self):                                         
        return self.email