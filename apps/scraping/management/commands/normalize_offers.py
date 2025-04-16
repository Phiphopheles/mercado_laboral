from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Normaliza las ofertas de empleo detectando tecnologías en la descripción.'

    def handle(self, *args, **kwargs):
        normalizador = None
        # Probar ambas rutas de importación
        try:
            from inteligencia.normalizador import normalizar_ofertas
            normalizador = normalizar_ofertas
            self.stdout.write('Importación vía inteligencia.normalizador OK.')
        except ImportError:
            try:
                from apps.inteligencia.normalizador import normalizar_ofertas
                normalizador = normalizar_ofertas
                self.stdout.write('Importación vía apps.inteligencia.normalizador OK.')
            except ImportError:
                self.stderr.write('No se pudo importar normalizar_ofertas. Asegúrate de que el archivo y la función existen.')
                return

        try:
            normalizador()
            self.stdout.write(self.style.SUCCESS('Normalización completada correctamente.'))
        except Exception as e:
            self.stderr.write(f'Error al normalizar las ofertas: {e}')
