from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OfertaEmpleoViewSet

router = DefaultRouter()
router.register(r'ofertas', OfertaEmpleoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
