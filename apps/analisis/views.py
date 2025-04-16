from rest_framework import viewsets
from .models import Habilidad
from .serializers import HabilidadSerializer
from django.shortcuts import render
from apps.scraping.models import OfertaEmpleo
from collections import Counter
from django.db.models import Count
import json
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from django.utils import timezone

@login_required
def analisis_tecnologias_view(request):
    ofertas = OfertaEmpleo.objects.all()
    
    # Contamos las habilidades asociadas
    habilidades_contadas = Counter()
    for oferta in ofertas.prefetch_related('habilidades'):
        for habilidad in oferta.habilidades.all():
            habilidades_contadas[habilidad.nombre] += 1

    top_habilidades = habilidades_contadas.most_common(10)
    
    labels = [h[0] for h in top_habilidades]
    data = [h[1] for h in top_habilidades]

    context = {
        'labels': json.dumps(labels),
        'data': json.dumps(data),
    }
    return render(request, 'analisis/tecnologias.html', context)

class HabilidadViewSet(viewsets.ModelViewSet):
    queryset = Habilidad.objects.all()
    serializer_class = HabilidadSerializer

def resumen_dashboard(request):
    resumen_por_plataforma = (
        OfertaEmpleo.objects.values("plataforma")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    resumen_por_fecha = (
        OfertaEmpleo.objects
        .filter(fecha_publicacion__gte=timezone.now() - timedelta(days=15))
        .extra(select={'day': "date(fecha_publicacion)"})
        .values("day")
        .annotate(count=Count("id"))
        .order_by("day")
    )

    return render(request, "analisis/dashboard.html", {
        "resumen_por_plataforma": list(resumen_por_plataforma),
        "resumen_por_fecha": list(resumen_por_fecha),
    })