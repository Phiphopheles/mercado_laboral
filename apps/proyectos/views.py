from django.shortcuts import render
from rest_framework import viewsets
from .models import Proyecto, Tarea
from .serializers import ProyectoSerializer, TareaSerializer
from django.contrib.auth.decorators import login_required

class ProyectoViewSet(viewsets.ModelViewSet):
    queryset = Proyecto.objects.all()
    serializer_class = ProyectoSerializer

class TareaViewSet(viewsets.ModelViewSet):
    queryset = Tarea.objects.all()
    serializer_class = TareaSerializer


@login_required
def dashboard_view(request):
    total_proyectos = Proyecto.objects.count()
    total_tareas = Tarea.objects.count()
    tareas = Tarea.objects.select_related('proyecto').order_by('-fecha_limite')[:10]  # últimas 10

    return render(request, 'proyectos/dashboard.html', {
        'total_proyectos': total_proyectos,
        'total_tareas': total_tareas,
        'tareas': tareas
    })