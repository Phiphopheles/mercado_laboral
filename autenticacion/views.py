from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

class CustomLoginView(LoginView):
    template_name = 'autenticacion/login.html'
    success_url = reverse_lazy('dashboard')
