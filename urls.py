from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/usuarios/', include('apps.autenticacion.urls')),
    path('api/proyectos/', include('apps.proyectos.urls')),
    path('api/analisis/', include('apps.analisis.urls')),
    path('api/scraping/', include('apps.scraping.urls')),
    path('api/inteligencia/', include('apps.inteligencia.urls')),
]
