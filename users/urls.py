from django.urls import path, include                                  
from rest_framework.routers import DefaultRouter                       
from .views import MeView, UserViewSet

router = DefaultRouter()                                                
router.register(r"users", UserViewSet, basename="users")
               

urlpatterns = [
    path("", include(router.urls)),
    path("auth/me/", MeView.as_view(), name="me"),
]