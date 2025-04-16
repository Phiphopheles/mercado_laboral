from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HabilidadViewSet
from .views import analisis_tecnologias_view
from . import views

router = DefaultRouter()
router.register(r'habilidades', HabilidadViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('tecnologias/', analisis_tecnologias_view, name='analisis_tecnologias'),
    path("dashboard/", views.resumen_dashboard, name="dashboard"),
]
