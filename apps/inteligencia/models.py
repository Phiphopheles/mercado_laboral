from django.db import models
from apps.autenticacion.models import Usuario
from apps.analisis.models import Habilidad
from apps.proyectos.models import Tarea

# Recomendaciones personalizadas de tareas para cada usuario
class RecomendacionTarea(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE)
    puntaje = models.FloatField(help_text="Puntaje de recomendación")

    generado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'tarea')

    def __str__(self):
        return f'Recomendación: {self.usuario.username} → {self.tarea.titulo}'


# Predicciones sobre habilidades futuras basadas en ofertas
class PrediccionHabilidad(models.Model):
    habilidad = models.ForeignKey(Habilidad, on_delete=models.CASCADE)
    fecha_prediccion = models.DateField()
    valor_estimado = models.FloatField(help_text="Popularidad estimada")

    generado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.habilidad.nombre} ({self.fecha_prediccion}): {self.valor_estimado}'
