from .base_scraper import BaseScraper
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import urllib.parse

class TecnoempleoScraper(BaseScraper):
    def __init__(self, headless=True):
        super().__init__(headless)
        self.base_url = "https://www.tecnoempleo.com"
        self.search_terms = [
            'python',
            'javascript',
            'java',
            'desarrollador web',
            'full stack',
            'devops',
            'data engineer'
        ]

    def scrape(self):
        jobs = []
        driver = self.get_driver()

        if driver is None:
            print("No se pudo inicializar el driver")
            return jobs

        try:
            for search_term in self.search_terms:
                try:
                    # Construir URL de búsqueda
                    encoded_term = urllib.parse.quote(search_term)
                    search_url = f"{self.base_url}/busqueda-empleo.php?te={encoded_term}&pr=true"
                    
                    # Navegar a la página
                    driver.get(search_url)
                    self.random_sleep(3, 5)

                    # Esperar a que carguen las ofertas
                    try:
                        WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, '.oferta'))
                        )
                    except TimeoutException:
                        print(f"No se encontraron ofertas para: {search_term}")
                        continue

                    # Buscar ofertas
                    job_listings = driver.find_elements(By.CSS_SELECTOR, '.oferta')

                    if not job_listings:
                        print(f"No se encontraron ofertas para: {search_term}")
                        continue

                    print(f"Encontradas {len(job_listings)} ofertas para: {search_term}")

                    # Procesar cada oferta
                    for job in job_listings[:10]:  # Limitar a 10 ofertas por búsqueda
                        try:
                            # Extraer título con selectores alternativos y logs
                            try:
                                try:
                                    title = job.find_element(By.CSS_SELECTOR, 'h2.titulo, h2, h3, .job-title, .titulo').text.strip()
                                except Exception:
                                    title = 'No encontrado'
                                print(f"[TECNOEMPLEO] Título extraído: {title}")
                            except Exception:
                                title = 'No encontrado'
                                print(f"[TECNOEMPLEO] Título NO encontrado")

                            # Extraer empresa
                            try:
                                company = job.find_element(By.CSS_SELECTOR, '.company, .empresa, .subtitle').text.strip()
                            except Exception:
                                company = 'Sin empresa'
                            print(f"[TECNOEMPLEO] Empresa extraída: {company}")

                            # Extraer ubicación
                            try:
                                location = job.find_element(By.CSS_SELECTOR, '.location, .ubicacion').text.strip()
                            except Exception:
                                location = 'España'
                            print(f"[TECNOEMPLEO] Ubicación extraída: {location}")

                            # Extraer descripción con selectores alternativos y logs
                            try:
                                description_elem = job.find_element(By.CSS_SELECTOR, '.description, .job-description, .oferta-description, .descripcion')
                                description = description_elem.text.strip()
                            except Exception:
                                description = ''
                            print(f"[TECNOEMPLEO] Descripción extraída: {description[:100]}...")

                            # Intentar obtener el enlace y descripción
                            try:
                                link = job.find_element(By.CSS_SELECTOR, 'h2.titulo a').get_attribute('href')
                                
                                # Abrir la oferta en una nueva pestaña
                                driver.execute_script(f"window.open('{link}', '_blank');")
                                self.random_sleep(1, 2)
                                
                                # Cambiar a la nueva pestaña
                                driver.switch_to.window(driver.window_handles[-1])
                                
                                # Esperar a que cargue la descripción
                                try:
                                    WebDriverWait(driver, 10).until(
                                        EC.presence_of_element_located((By.CSS_SELECTOR, '.contenido-oferta'))
                                    )
                                    description = driver.find_element(By.CSS_SELECTOR, '.contenido-oferta').text.strip()
                                    if description:
                                        title = f"{title} - {description[:100]}..."
                                except:
                                    pass

                                # Cerrar la pestaña y volver a la búsqueda
                                driver.close()
                                driver.switch_to.window(driver.window_handles[0])
                            except:
                                pass

                            jobs.append({
                                'titulo': title,
                                'empresa': company,
                                'ubicacion': location,
                                'fecha_publicacion': datetime.now().strftime("%Y-%m-%d"),
                                'portal': 'Tecnoempleo',
                                'descripcion': description
                            })

                            print(f"Procesada oferta: {title} | {company}")
                            self.random_sleep(1, 2)

                        except Exception as e:
                            print(f"Error procesando oferta: {str(e)}")
                            continue

                    self.random_sleep(3, 5)

                except Exception as e:
                    print(f"Error en búsqueda {search_term}: {str(e)}")
                    continue

        except Exception as e:
            print(f"Error general: {str(e)}")

        finally:
            self.close()

        return jobs
