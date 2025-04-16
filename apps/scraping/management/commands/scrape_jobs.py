from django.core.management.base import BaseCommand
from apps.scraping.models import OfertaEmpleo
from apps.scraping.scrapers.tecnoempleo_scraper import TecnoempleoScraper
from apps.scraping.scrapers.infojobs_scraper import InfojobsScraper
from apps.scraping.scrapers.linkedin_scraper import LinkedinScraper
import random

class Command(BaseCommand):
    help = 'Scrapea ofertas de empleo de varios portales usando Selenium'

    def add_arguments(self, parser):
        parser.add_argument(
            '--portales',
            nargs='+',
            type=str,
            help='Lista de portales a scrapear (tecnoempleo, infojobs, linkedin)'
        )
        parser.add_argument(
            '--headless',
            action='store_true',
            help='Ejecutar en modo headless (sin interfaz gráfica)'
        )

    def handle(self, *args, **options):
        portales = options['portales'] or ['tecnoempleo', 'infojobs', 'linkedin']
        headless = options['headless']
        
        self.stdout.write("🌐 Iniciando scraping de ofertas de empleo...")
        
        scrapers = {
            'tecnoempleo': TecnoempleoScraper(headless=headless),
            'infojobs': InfojobsScraper(headless=headless),
            'linkedin': LinkedinScraper(headless=headless)
        }
        
        total_ofertas = 0
        
        # Mezclar el orden de los portales para no seguir siempre el mismo patrón
        portales_seleccionados = [p for p in portales if p in scrapers]
        random.shuffle(portales_seleccionados)
        
        for portal in portales_seleccionados:
            try:
                self.stdout.write(f"\n🔍 Scrapeando {portal.title()}...")
                scraper = scrapers[portal]
                jobs = scraper.scrape()
                
                if not jobs:
                    self.stdout.write(self.style.WARNING(f"⚠️ No se encontraron ofertas en {portal}"))
                    continue
                
                self.stdout.write(f"📝 Guardando {len(jobs)} ofertas de {portal}...")
                
                for job in jobs:
                    try:
                        OfertaEmpleo.objects.create(**job)
                        total_ofertas += 1
                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR(f"❌ Error guardando oferta: {str(e)}")
                        )
                
                self.stdout.write(
                    self.style.SUCCESS(f"✅ Completado {portal}: {len(jobs)} ofertas")
                )
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"❌ Error en {portal}: {str(e)}")
                )
        
        if total_ofertas > 0:
            self.stdout.write(
                self.style.SUCCESS(f"\n✅ Scraping completado: {total_ofertas} ofertas guardadas")
            )
        else:
            self.stdout.write(
                self.style.WARNING("\n⚠️ No se pudo guardar ninguna oferta")
            )
