from django.contrib import admin                                      
from django.urls import path, include                                
from rest_framework_simplejwt.views import (                          
    TokenObtainPairView, TokenRefreshView
)
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Portfolio Backend API",
        default_version="v1",
        description=(
            "API REST desarrollada en Django Rest Framework para autenticación JWT, "
            "roles, permisos y gestión de usuarios.\n\n"
            "## Autenticación\n"
            "1️ `/api/v1/token/` → obtener tokens (access/refresh)\n"
            "2️ Añadir header: `Authorization: Bearer <access_token>`\n\n"
            "## Recursos\n"
            "- `/api/v1/users/` → CRUD de usuarios\n"
            "- `/api/v1/roles/` → CRUD de roles\n"
            "- `/api/v1/permissions/` → CRUD de permisos\n"
            "- `/api/v1/auth/me/` → datos del usuario autenticado\n\n"
            "## Formato de respuesta\n"
            "{\n"
            "  \"success\": true|false,\n"
            "  \"message\": \"Texto descriptivo\",\n"
            "  \"data\": {...} | null,\n"
            "  \"errors\": {...} | null\n"
            "}"
        ),
        
        contact=openapi.Contact(email="juanfelipealvearestrada@gmail.com"),
        license=openapi.License(name="Todos los derechos reservados"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    
    patterns=[
        path("api/v1/", include("users.urls")),
        path("api/v1/", include("roles.urls")),
        path("api/v1/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
        path("api/v1/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    ],
)

urlpatterns = [
    path("admin/", admin.site.urls),

    
    path("", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),

    
    path("api/v1/", include("users.urls")),
    path("api/v1/", include("roles.urls")),
    path("api/v1/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/v1/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]