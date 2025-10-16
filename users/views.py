from rest_framework import viewsets, status                                   
from rest_framework.response import Response                                  
from rest_framework.permissions import IsAuthenticated, AllowAny  
from rest_framework_simplejwt.views import TokenObtainPairView   
from rest_framework.views import APIView                    
from .models import CustomUser                           
from .serializers import (                                                   
    UserReadSerializer, UserWriteSerializer, MyTokenObtainPairSerializer,
)


from rest_framework.pagination import PageNumberPagination                     
from django_filters.rest_framework import DjangoFilterBackend                  
from rest_framework import filters  

# Create your views here.
class StandardResultsSetPagination(PageNumberPagination):                      
    page_size = 10                                                           
    page_size_query_param = "page_size"                                       
    max_page_size = 100                                                       



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

class UserViewSet(ApiResponseMixin, viewsets.ModelViewSet):                    
    queryset = CustomUser.objects.all()                                       
    permission_classes = [IsAuthenticated]                                     
    pagination_class = StandardResultsSetPagination                            

   
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter] 
    filterset_fields = ["email", "first_name", "last_name", "role"]         
    search_fields = ["email", "first_name", "last_name"]                    
    ordering_fields = ["id", "email", "first_name", "last_name"]             
    ordering = ["id"]                                                       

    def get_serializer_class(self):                                           
        if self.action in ["list", "retrieve"]:                              
            return UserReadSerializer                                        
        return UserWriteSerializer                                           

    def list(self, request, *args, **kwargs):                                
        queryset = self.filter_queryset(self.get_queryset())                  
        page = self.paginate_queryset(queryset)                              
        if page is not None:                                                 
            serializer = self.get_serializer(page, many=True)                 
            
            data = {
                "count": self.paginator.page.paginator.count,                
                "next": self.paginator.get_next_link(),                       
                "previous": self.paginator.get_previous_link(),              
                "results": serializer.data,                                  
            }
            return self.success_response(data, message="Listado de usuarios") 
        
        serializer = self.get_serializer(queryset, many=True)                
        return self.success_response(serializer.data, message="Listado de usuarios (sin paginar)")  

    def retrieve(self, request, *args, **kwargs):                             # GET /users/{id}/
        instance = self.get_object()                                          
        serializer = self.get_serializer(instance)                           
        return self.success_response(serializer.data, message="Detalle de usuario")  

    def create(self, request, *args, **kwargs):                                # POST /users/
        serializer = self.get_serializer(data=request.data)                  
        if not serializer.is_valid():                                         
            return self.error_response(serializer.errors, message="Datos inválidos")  
        self.perform_create(serializer)                                      
        read_serializer = UserReadSerializer(serializer.instance)             
        return self.success_response(read_serializer.data,                    
                                     message="Usuario creado",
                                     status_code=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):                                # PUT /users/{id}/
        partial = kwargs.pop("partial", False)                                
        instance = self.get_object()                                         
        serializer = self.get_serializer(instance, data=request.data, partial=partial)  
        if not serializer.is_valid():                                        
            return self.error_response(serializer.errors, message="Datos inválidos")    
        self.perform_update(serializer)                                       
        read_serializer = UserReadSerializer(serializer.instance)             
        return self.success_response(read_serializer.data, message="Usuario actualizado")  

    def destroy(self, request, *args, **kwargs):                               # DELETE /users/{id}/
        instance = self.get_object()                                       
        self.perform_destroy(instance)                                       
        return self.success_response(None, message="Usuario eliminado", status_code=status.HTTP_204_NO_CONTENT)  
    

class MeView(ApiResponseMixin, APIView):                                      
    permission_classes = [IsAuthenticated]                                     

    def get(self, request):                                                    # GET /api/auth/me/
        user = request.user                                                    
        serializer = UserReadSerializer(user)                                  
        return self.success_response(serializer.data, message="Perfil del usuario autenticado")  


class MyTokenObtainPairView(ApiResponseMixin, TokenObtainPairView):           
    serializer_class = MyTokenObtainPairSerializer                             

    def post(self, request, *args, **kwargs):                                   # POST /api/token/
        serializer = self.get_serializer(data=request.data)                   
        try:
            serializer.is_valid(raise_exception=True)                        
        except Exception as exc:                                               
            return self.error_response({"detail": "Credenciales inválidas"},   
                                       message="No autorizado",                
                                       status_code=status.HTTP_401_UNAUTHORIZED)  

       
        return self.success_response(serializer.data,                          
                                     message="Login exitoso",                  
                                     status_code=status.HTTP_200_OK)   
        print(serializer.data)