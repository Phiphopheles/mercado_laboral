from django.db import models
from apps.analisis.models import Habilidad

class OfertaEmpleo(models.Model):
    portal = models.CharField(max_length=50)  # InfoJobs, LinkedIn, Tecnoempleo
    titulo = models.CharField(max_length=255)
    empresa = models.CharField(max_length=255)
    ubicacion = models.CharField(max_length=255)
    salario = models.CharField(max_length=50, null=True, blank=True)
    fecha_publicacion = models.DateField()
    habilidades = models.ManyToManyField(Habilidad, related_name='ofertas')
    descripcion = models.TextField(blank=True, null=True)  
    tecnologias = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.titulo} - {self.empresa} ({self.portal})'
