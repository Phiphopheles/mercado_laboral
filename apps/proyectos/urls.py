from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProyectoViewSet, TareaViewSet

router = DefaultRouter()
router.register(r'proyectos', ProyectoViewSet)
router.register(r'tareas', TareaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
