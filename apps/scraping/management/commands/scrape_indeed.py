from django.core.management.base import BaseCommand
from apps.scraping.models import OfertaEmpleo
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import random

class Command(BaseCommand):
    help = 'Scrapea ofertas de empleo desde Indeed usando su versión móvil'

    def get_random_user_agent(self):
        user_agents = [
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36',
            'Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Linux; Android 10; SM-A505FN) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36'
        ]
        return random.choice(user_agents)

    def handle(self, *args, **options):
        self.stdout.write("🌐 Iniciando scraping desde Indeed...")

        try:
            # Configurar la sesión
            session = requests.Session()
            session.headers.update({
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            })

            # Búsquedas a realizar
            searches = [
                {'q': 'python developer', 'l': 'España'},
                {'q': 'desarrollador web', 'l': 'España'},
                {'q': 'programador', 'l': 'España'},
                {'q': 'software engineer', 'l': 'España'}
            ]

            total_ofertas = 0

            for search in searches:
                try:
                    # Actualizar User-Agent para cada búsqueda
                    session.headers['User-Agent'] = self.get_random_user_agent()
                    
                    # Construir URL de búsqueda
                    params = {
                        'q': search['q'],
                        'l': search['l'],
                        'sort': 'date',  # Ordenar por fecha
                        'filter': '0',    # Sin filtros
                        'vjk': '1'        # Vista móvil
                    }
                    
                    url = 'https://es.indeed.com/jobs'
                    
                    self.stdout.write(f"Buscando: {search['q']} en {search['l']}")
                    response = session.get(url, params=params)
                    
                    if response.status_code != 200:
                        self.stdout.write(self.style.WARNING(f"⚠️ Error en la búsqueda: {response.status_code}"))
                        continue

                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Buscar ofertas
                    ofertas = soup.select('.job_seen_beacon')
                    
                    if not ofertas:
                        self.stdout.write(f"No se encontraron ofertas para {search['q']}")
                        continue

                    self.stdout.write(f"📝 Encontradas {len(ofertas)} ofertas")

                    # Procesar las primeras 5 ofertas de cada búsqueda
                    for oferta in ofertas[:5]:
                        try:
                            # Extraer información
                            titulo_elem = oferta.select_one('.jobTitle')
                            titulo = titulo_elem.get_text(strip=True) if titulo_elem else 'Sin título'
                            
                            empresa_elem = oferta.select_one('.companyName')
                            empresa = empresa_elem.get_text(strip=True) if empresa_elem else 'Sin empresa'
                            
                            ubicacion_elem = oferta.select_one('.companyLocation')
                            ubicacion = ubicacion_elem.get_text(strip=True) if ubicacion_elem else 'España'

                            self.stdout.write(f"Procesando oferta: {titulo} | {empresa}")

                            # Guardar en la base de datos
                            OfertaEmpleo.objects.create(
                                titulo=titulo,
                                empresa=empresa,
                                ubicacion=ubicacion,
                                fecha_publicacion=datetime.now().strftime("%Y-%m-%d"),
                                portal='Indeed'
                            )

                            total_ofertas += 1
                            self.stdout.write(self.style.SUCCESS(f"✅ Guardada oferta: {titulo}"))
                            
                            # Espera aleatoria entre ofertas
                            time.sleep(random.uniform(2, 3))

                        except Exception as e:
                            self.stdout.write(self.style.ERROR(f"❌ Error procesando oferta: {str(e)}"))

                    # Espera entre búsquedas
                    time.sleep(random.uniform(3, 5))

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"❌ Error en búsqueda: {str(e)}"))

            if total_ofertas == 0:
                self.stdout.write(self.style.WARNING("⚠️ No se encontraron ofertas"))
            else:
                self.stdout.write(self.style.SUCCESS(f"✅ Se guardaron {total_ofertas} ofertas en total"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error general: {str(e)}"))
            self.stdout.write(str(e))
        
        self.stdout.write(self.style.SUCCESS("✅ Scraping completado."))
