from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RecomendacionTareaViewSet, PrediccionHabilidadViewSet

router = DefaultRouter()
router.register(r'recomendaciones', RecomendacionTareaViewSet)
router.register(r'predicciones', PrediccionHabilidadViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
