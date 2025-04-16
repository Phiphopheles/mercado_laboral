from rest_framework import viewsets
from .models import RecomendacionTarea, PrediccionHabilidad
from .serializers import RecomendacionTareaSerializer, PrediccionHabilidadSerializer

class RecomendacionTareaViewSet(viewsets.ModelViewSet):
    queryset = RecomendacionTarea.objects.all()
    serializer_class = RecomendacionTareaSerializer

class PrediccionHabilidadViewSet(viewsets.ModelViewSet):
    queryset = PrediccionHabilidad.objects.all()
    serializer_class = PrediccionHabilidadSerializer
