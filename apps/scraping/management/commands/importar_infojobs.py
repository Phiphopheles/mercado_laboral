from django.core.management.base import BaseCommand
from scraping.scraper_infojobs import scrap_infojobs

class Command(BaseCommand):
    help = "Importa ofertas desde InfoJobs vía scraping"

    def handle(self, *args, **kwargs):
        scrap_infojobs()
