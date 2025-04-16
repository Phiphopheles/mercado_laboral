from django.core.management.base import BaseCommand
from apps.scraping.models import OfertaEmpleo
import feedparser
from datetime import datetime
import time
import random

class Command(BaseCommand):
    help = 'Scrapea ofertas de empleo desde InfoJobs usando su feed RSS'

    def handle(self, *args, **options):
        self.stdout.write("🌐 Iniciando scraping desde InfoJobs RSS...")

        try:
            # URLs de feeds RSS de InfoJobs
            feeds = [
                'https://www.infojobs.net/ofertas-trabajo/informatica-telecomunicaciones/rss',
                'https://www.infojobs.net/ofertas-trabajo/programacion/rss',
                'https://www.infojobs.net/ofertas-trabajo/desarrollo-software/rss'
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
                        empresa = "InfoJobs"  # Por defecto
                        
                        # Intentar extraer la empresa de la descripción
                        if " - " in descripcion:
                            partes = descripcion.split(" - ")
                            if len(partes) > 1:
                                empresa = partes[0].strip()
                        
                        # La ubicación suele estar en la descripción
                        ubicacion = "España"  # Por defecto
                        for parte in descripcion.split(" - "):
                            # Si la parte contiene palabras comunes de ubicación
                            if any(ciudad in parte.lower() for ciudad in ["madrid", "barcelona", "valencia", "sevilla", "bilbao"]):
                                ubicacion = parte.strip()
                                break
                        
                        self.stdout.write(f"Procesando oferta: {titulo} | {empresa}")

                        # Guardar en la base de datos
                        OfertaEmpleo.objects.create(
                            titulo=titulo,
                            empresa=empresa,
                            ubicacion=ubicacion,
                            fecha_publicacion=datetime.now().strftime("%Y-%m-%d"),
                            portal='InfoJobs'
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
