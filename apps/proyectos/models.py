from django.db import models
from apps.autenticacion.models import Usuario

class Proyecto(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    gestor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='proyectos')

    def __str__(self):
        return self.nombre


class Tarea(models.Model):
    PENDIENTE = 'pendiente'
    EN_PROGRESO = 'en_progreso'
    COMPLETADA = 'completada'

    ESTADOS = [
        (PENDIENTE, 'Pendiente'),
        (EN_PROGRESO, 'En Progreso'),
        (COMPLETADA, 'Completada'),
    ]

    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default=PENDIENTE)
    prioridad = models.IntegerField(default=1)
    fecha_limite = models.DateField()
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='tareas')
    asignado_a = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='tareas')

    def __str__(self):
        return f'{self.titulo} ({self.get_estado_display()})'
