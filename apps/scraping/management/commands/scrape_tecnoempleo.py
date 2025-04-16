from django.core.management.base import BaseCommand
from apps.scraping.models import OfertaEmpleo
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import random

class Command(BaseCommand):
    help = 'Scrapea ofertas de empleo desde Tecnoempleo usando rotación de User-Agents'

    def get_random_user_agent(self):
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36'
        ]
        return random.choice(user_agents)

    def handle(self, *args, **options):
        self.stdout.write("🌐 Iniciando scraping con rotación de User-Agents...")

        try:
            # Crear una sesión para mantener cookies
            with requests.Session() as session:
                # Configurar headers base
                session.headers.update({
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'DNT': '1',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                    'Sec-Fetch-Dest': 'document',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'none',
                    'Sec-Fetch-User': '?1',
                    'Cache-Control': 'max-age=0'
                })

                # URLs a intentar
                urls = [
                    'https://www.tecnoempleo.com/ofertas-trabajo/?cp=1',
                    'https://www.tecnoempleo.com/ofertas-trabajo/informatica-telecomunicaciones/?cp=1',
                    'https://www.tecnoempleo.com/ofertas-trabajo/programacion/?cp=1',
                    'https://www.tecnoempleo.com/ofertas-trabajo/desarrollo-web/?cp=1'
                ]

                for url in urls:
                    # Actualizar User-Agent para cada petición
                    session.headers['User-Agent'] = self.get_random_user_agent()
                    
                    self.stdout.write(f"Accediendo a {url}...")
                    response = session.get(url)
                    
                    if response.status_code != 200:
                        self.stdout.write(self.style.WARNING(f"⚠️ Error al acceder a {url}: {response.status_code}"))
                        continue

                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Intentar diferentes selectores para las ofertas
                    ofertas = []
                    for selector in [
                        'article.job-item',
                        'div.job-item',
                        'div.oferta',
                        'div[data-job-id]',
                        'div.box-oferta',
                        'div.item-empleo'
                    ]:
                        ofertas.extend(soup.select(selector))

                    if ofertas:
                        self.stdout.write(f"📝 Encontradas {len(ofertas)} ofertas en {url}")
                        break
                    else:
                        self.stdout.write(f"No se encontraron ofertas en {url}")
                        time.sleep(random.uniform(2, 4))
                        continue

                if not ofertas:
                    self.stdout.write(self.style.WARNING("⚠️ No se encontraron ofertas en ninguna URL"))
                    return

                # Procesar las primeras 10 ofertas
                for oferta in ofertas[:10]:
                    try:
                        # Intentar varios selectores para el título
                        titulo_elem = (
                            oferta.select_one('h2.job-title') or
                            oferta.select_one('h3.job-title') or
                            oferta.select_one('a[title]') or
                            oferta.select_one('h2') or
                            oferta.select_one('h3') or
                            oferta.select_one('a.titulo') or
                            oferta.select_one('.titulo')
                        )
                        titulo = titulo_elem.get_text(strip=True) if titulo_elem else 'Sin título'

                        # Intentar varios selectores para la empresa
                        empresa_elem = (
                            oferta.select_one('.company-name') or
                            oferta.select_one('.empresa') or
                            oferta.select_one('[data-company]') or
                            oferta.select_one('.nombreEmpresa')
                        )
                        empresa = empresa_elem.get_text(strip=True) if empresa_elem else 'Sin empresa'

                        # Intentar varios selectores para la ubicación
                        ubicacion_elem = (
                            oferta.select_one('.location') or
                            oferta.select_one('.ubicacion') or
                            oferta.select_one('[data-location]') or
                            oferta.select_one('.ciudad')
                        )
                        ubicacion = ubicacion_elem.get_text(strip=True) if ubicacion_elem else 'Sin ubicación'

                        # Intentar obtener el enlace y más detalles
                        try:
                            enlace = titulo_elem.get('href') if titulo_elem and titulo_elem.name == 'a' else oferta.select_one('a').get('href')
                            if enlace and not enlace.startswith('http'):
                                enlace = f'https://www.tecnoempleo.com{enlace}'
                            
                            # Esperar un tiempo aleatorio antes de la siguiente petición
                            time.sleep(random.uniform(2, 4))
                            
                            # Actualizar User-Agent para cada petición
                            session.headers['User-Agent'] = self.get_random_user_agent()
                            
                            # Obtener detalles de la oferta
                            detalle_response = session.get(enlace)
                            if detalle_response.status_code == 200:
                                detalle_soup = BeautifulSoup(detalle_response.text, 'html.parser')
                                descripcion = detalle_soup.select_one('.job-description, .description, .contenido')
                                if descripcion:
                                    titulo = f"{titulo} - {descripcion.get_text(strip=True)[:100]}..."
                        except Exception as e:
                            self.stdout.write(f"⚠️ No se pudo obtener detalles adicionales: {str(e)}")

                        self.stdout.write(f"Procesando oferta: {titulo} | {empresa}")

                        # Guardar en la base de datos
                        OfertaEmpleo.objects.create(
                            titulo=titulo,
                            empresa=empresa,
                            ubicacion=ubicacion,
                            fecha_publicacion=datetime.now().strftime("%Y-%m-%d"),
                            portal='Tecnoempleo'
                        )

                        self.stdout.write(self.style.SUCCESS(f"✅ Guardada oferta: {titulo}"))
                        
                        # Espera aleatoria entre ofertas
                        time.sleep(random.uniform(2, 4))

                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"❌ Error procesando oferta: {str(e)}"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error general: {str(e)}"))
            self.stdout.write(str(e))
        
        self.stdout.write(self.style.SUCCESS("✅ Scraping completado."))
