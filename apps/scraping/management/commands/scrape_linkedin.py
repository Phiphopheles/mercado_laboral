from django.core.management.base import BaseCommand
from apps.scraping.models import OfertaEmpleo
import feedparser
from datetime import datetime
import time
import random

class Command(BaseCommand):
    help = 'Scrapea ofertas de empleo desde LinkedIn usando su feed RSS'

    def handle(self, *args, **options):
        self.stdout.write("🌐 Iniciando scraping desde LinkedIn RSS...")

        try:
            # URLs de feeds RSS de LinkedIn
            # Estos feeds son públicos y no requieren autenticación
            feeds = [
                'https://www.linkedin.com/jobs/search?keywords=python&location=España&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&f_TPR=r86400&redirect=false&rss=true',
                'https://www.linkedin.com/jobs/search?keywords=desarrollador%20web&location=España&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&f_TPR=r86400&redirect=false&rss=true',
                'https://www.linkedin.com/jobs/search?keywords=software%20engineer&location=España&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&f_TPR=r86400&redirect=false&rss=true'
            ]

            total_ofertas = 0

            for feed_url in feeds:
                self.stdout.write(f"Accediendo a feed: {feed_url}")
                
                # Parsear el feed RSS
                feed = feedparser.parse(feed_url)
                
                if not feed.entries:
                    self.stdout.write(f"No se encontraron ofertas en {feed_url}")
                    continue

                self.stdout.write(f"📝 Encontradas {len(feed.entries)} ofertas en el feed")
                
                # Procesar las primeras 10 ofertas de cada feed
                for entry in feed.entries[:10]:
                    try:
                        titulo = entry.title
                        
                        # La descripción puede contener el nombre de la empresa
                        descripcion = entry.description
                        empresa = "LinkedIn"  # Por defecto
                        
                        # Intentar extraer la empresa del título
                        if " at " in titulo:
                            titulo, empresa = titulo.split(" at ", 1)
                        
                        # La ubicación suele estar en la descripción
                        ubicacion = "España"  # Por defecto
                        if "location" in entry:
                            ubicacion = entry.location
                        
                        self.stdout.write(f"Procesando oferta: {titulo} | {empresa}")

                        # Guardar en la base de datos
                        OfertaEmpleo.objects.create(
                            titulo=titulo,
                            empresa=empresa,
                            ubicacion=ubicacion,
                            fecha_publicacion=datetime.now().strftime("%Y-%m-%d"),
                            portal='LinkedIn'
                        )

                        total_ofertas += 1
                        self.stdout.write(self.style.SUCCESS(f"✅ Guardada oferta: {titulo}"))
                        
                        # Espera aleatoria entre ofertas
                        time.sleep(random.uniform(1, 2))

                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"❌ Error procesando oferta: {str(e)}"))

                # Espera entre feeds
                time.sleep(random.uniform(2, 3))

            if total_ofertas == 0:
                self.stdout.write(self.style.WARNING("⚠️ No se encontraron ofertas en ningún feed"))
            else:
                self.stdout.write(self.style.SUCCESS(f"✅ Se guardaron {total_ofertas} ofertas en total"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error general: {str(e)}"))
            self.stdout.write(str(e))
        
        self.stdout.write(self.style.SUCCESS("✅ Scraping completado."))
