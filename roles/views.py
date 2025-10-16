from rest_framework import viewsets, status                                  
from rest_framework.response import Response                                
from rest_framework.permissions import IsAuthenticated                      
from .models import  Role, Permission                             
from .serializers import (                                                  
    RoleReadSerializer, RoleWriteSerializer,
    PermissionReadSerializer,
)

# Create your views here.
class ApiResponseMixin:                                                       
    def success_response(self, data, message="OK", status_code=status.HTTP_200_OK):
        
        return Response(
            {"success": True, "message": message, "data": data, "errors": None},
            status=status_code,
        )

    def error_response(self, errors, message="Error", status_code=status.HTTP_400_BAD_REQUEST):
        
        return Response(
            {"success": False, "message": message, "data": None, "errors": errors},
            status=status_code,
        )

class RoleViewSet(ApiResponseMixin, viewsets.ModelViewSet):                   
    queryset = Role.objects.all()                                            
    permission_classes = [IsAuthenticated]                                    

    def get_serializer_class(self):                                          
        if self.action in ["list", "retrieve"]:                              
            return RoleReadSerializer                                        
        return RoleWriteSerializer                                           

    def list(self, request, *args, **kwargs):                                 # GET /roles/
        queryset = self.filter_queryset(self.get_queryset())                  
        serializer = self.get_serializer(queryset, many=True)                 
        return self.success_response(serializer.data, message="Listado de roles")     

    def retrieve(self, request, *args, **kwargs):                             # GET /roles/{id}/
        instance = self.get_object()                                          
        serializer = self.get_serializer(instance)                            
        return self.success_response(serializer.data, message="Detalle de rol")        

    def create(self, request, *args, **kwargs):                                # POST /roles/
        serializer = self.get_serializer(data=request.data)                  
        if not serializer.is_valid():                                         
            return self.error_response(serializer.errors, message="Datos inválidos")  
        instance = serializer.save()                                          
        read_serializer = RoleReadSerializer(instance)                       
        return self.success_response(read_serializer.data,                    
                                     message="Rol creado",
                                     status_code=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):                                # PUT /roles/{id}/
        partial = kwargs.pop("partial", False)                                
        instance = self.get_object()                                        
        serializer = self.get_serializer(instance, data=request.data, partial=partial) 
        if not serializer.is_valid():                                         
            return self.error_response(serializer.errors, message="Datos inválidos")   
        instance = serializer.save()                                          
        read_serializer = RoleReadSerializer(instance)                       
        return self.success_response(read_serializer.data, message="Rol actualizado")  

    def destroy(self, request, *args, **kwargs):                               # DELETE /roles/{id}/
        instance = self.get_object()                                          
        self.perform_destroy(instance)                                       
        return self.success_response(None, message="Rol eliminado", status_code=status.HTTP_204_NO_CONTENT)     



class PermissionViewSet(ApiResponseMixin, viewsets.ModelViewSet):             
    queryset = Permission.objects.all()                                       
    serializer_class = PermissionReadSerializer                              
    permission_classes = [IsAuthenticated]                                    

    
    def create(self, request, *args, **kwargs):                                # POST /permissions/
        serializer = PermissionReadSerializer(data=request.data)              
        if not serializer.is_valid():                                         
            return self.error_response(serializer.errors, message="Datos inválidos")   
        instance = serializer.save()                                         
        read_serializer = PermissionReadSerializer(instance)                
        return self.success_response(read_serializer.data, message="Permiso creado", status_code=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):                                # PUT /permissions/{id}/
        partial = kwargs.pop("partial", False)                               
        instance = self.get_object()                                         
        serializer = PermissionReadSerializer(instance, data=request.data, partial=partial) 
        if not serializer.is_valid():                                         
            return self.error_response(serializer.errors, message="Datos inválidos")   
        instance = serializer.save()                                         
        read_serializer = PermissionReadSerializer(instance)                  
        return self.success_response(read_serializer.data, message="Permiso actualizado")  

    def destroy(self, request, *args, **kwargs):                               # DELETE /permissions/{id}/
        instance = self.get_object()                                          
        self.perform_destroy(instance)                                     
        return self.success_response(None, message="Permiso eliminado", status_code=status.HTTP_204_NO_CONTENT)  