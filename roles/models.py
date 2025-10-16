from django.db import models

# Create your models here.
class Permission(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):                                         
        return self.name

class Role(models.Model):                                     
    name = models.CharField(max_length=100, unique=True)       
    permissions = models.ManyToManyField(                      
        Permission, related_name="roles", blank=True
    )

    def __str__(self):                                        
        return self.name