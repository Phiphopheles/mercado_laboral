from rest_framework import viewsets
from .models import OfertaEmpleo
from .serializers import OfertaEmpleoSerializer

class OfertaEmpleoViewSet(viewsets.ModelViewSet):
    queryset = OfertaEmpleo.objects.all()
    serializer_class = OfertaEmpleoSerializer
