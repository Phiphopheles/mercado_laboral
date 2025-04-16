from rest_framework import viewsets
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .models import Usuario
from .serializers import UsuarioSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class CustomLoginView(LoginView):
    template_name = 'autenticacion/login.html'
    success_url = reverse_lazy('dashboard')
    redirect_authenticated_user = True
