from django.core.management.base import BaseCommand
from apps.scraping.scrapers.infojobs_scraper import InfojobsScraper
from apps.scraping.scrapers.tecnoempleo_scraper import TecnoempleoScraper
from apps.scraping.scrapers.linkedin_scraper import LinkedinScraper

class Command(BaseCommand):
    help = 'Ejecuta todos los scrapers'

    def handle(self, *args, **kwargs):
        scrapers = [
            ('Infojobs', InfojobsScraper()),
            ('Tecnoempleo', TecnoempleoScraper()),
            ('LinkedIn', LinkedinScraper())
        ]

        for name, scraper in scrapers:
            print(f"\n🔍 Scrapeando {name}...")
            try:
                jobs = scraper.scrape()
                print(f"✅ Completado {name}: {len(jobs)} ofertas")
            except Exception as e:
                print(f"❌ Error en {name}: {str(e)}")

        print("\n✅ Scraping completado")
