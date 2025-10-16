from rest_framework import serializers
from .models import Permission, Role

class PermissionReadSerializer(serializers.ModelSerializer):               
    class Meta:                                                            
        model = Permission                                                
        fields = ["id", "name"]                                            



class RoleReadSerializer(serializers.ModelSerializer):                     
    permissions = PermissionReadSerializer(many=True, read_only=True)      

    class Meta:                                                            
        model = Role                                                      
        fields = ["id", "name", "permissions"]                             



class RoleWriteSerializer(serializers.ModelSerializer):                    
    permissions_ids = serializers.PrimaryKeyRelatedField(                 
        queryset=Permission.objects.all(), many=True, write_only=True, required=False
    )

    class Meta:                                                           
        model = Role                                                    
        fields = ["id", "name", "permissions_ids"]                         

    def create(self, validated_data):                                      
        perms = validated_data.pop("permissions_ids", [])                  
        role = Role.objects.create(**validated_data)                       
        if perms:                                                          
            role.permissions.set(perms)                                    
        return role                                                        

    def update(self, instance, validated_data):                             
        perms = validated_data.pop("permissions_ids", None)                
        for attr, value in validated_data.items():                         
            setattr(instance, attr, value)
        instance.save()                                                    
        if perms is not None:                                              
            instance.permissions.set(perms)                               
        return instance    