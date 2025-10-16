from rest_framework import serializers 
from django.contrib.auth.hashers import make_password
from .models import CustomUser
from roles.models import Role, Permission
from roles.serializers import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserReadSerializer(serializers.ModelSerializer):
    role = RoleReadSerializer(read_only = True)
    
    class Meta:
        model = CustomUser
        fields = ["id", "email", "first_name", "last_name", "role"]

class UserWriteSerializer(serializers.ModelSerializer):                    
    role_id = serializers.PrimaryKeyRelatedField(                          
        queryset=Role.objects.all(), source="role", write_only=True, required=False
    )

    class Meta:                                                           
        model = CustomUser                                                
        fields = ["id", "email", "first_name", "last_name", "password", "role_id"] 
        extra_kwargs = {                                                  
            "password": {"write_only": True, "min_length": 6},             
        }

    def create(self, validated_data):                                      
        if "password" in validated_data:                                  
            validated_data["password"] = make_password(                    
                validated_data["password"]
            )
        return super().create(validated_data)                             

    def update(self, instance, validated_data):                           
        if "password" in validated_data and validated_data["password"]:    
            validated_data["password"] = make_password(                    
                validated_data["password"]
            )
        else:
            validated_data.pop("password", None)                          
        return super().update(instance, validated_data)                    
    

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):             
    def validate(self, attrs):                                            
        data = super().validate(attrs)                                   
        user = self.user                                                  

        
        role_name = user.role.name if user.role else None               
        perms = []                                                        
        if user.role:                                                    
            perms = list(                                                 
                user.role.permissions.values("id", "name")
            )

        
        data.update({                                                    
            "user": {                                                    
                "id": user.id,                                             
                "email": user.email,                                   
                "first_name": user.first_name,                            
                "last_name": user.last_name,                              
                "role": role_name,                                        
                "permissions": perms,                                      
            }
        })
        return data           