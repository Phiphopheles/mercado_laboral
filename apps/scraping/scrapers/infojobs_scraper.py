from .base_scraper import BaseScraper
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import urllib.parse

class InfojobsScraper(BaseScraper):
    def __init__(self, headless=True):
        super().__init__(headless)
        self.base_url = "https://www.infojobs.net"
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
                    search_url = f"{self.base_url}/ofertas-trabajo/{encoded_term}"
                    
                    # Navegar a la página
                    driver.get(search_url)
                    self.random_sleep(3, 5)

                    # Esperar a que carguen las ofertas
                    try:
                        WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, '.ij-OfferCardContent'))
                        )
                    except TimeoutException:
                        print(f"No se encontraron ofertas para: {search_term}")
                        continue

                    # Buscar ofertas
                    job_listings = driver.find_elements(By.CSS_SELECTOR, '.ij-OfferCardContent')

                    if not job_listings:
                        print(f"No se encontraron ofertas para: {search_term}")
                        continue

                    print(f"Encontradas {len(job_listings)} ofertas para: {search_term}")

                    # Procesar cada oferta
                    for job in job_listings[:10]:  # Limitar a 10 ofertas por búsqueda
                        try:
                            # Extraer información básica con selectores alternativos y logs
                            try:
                                try:
                                    title = job.find_element(By.CSS_SELECTOR, '.ij-OfferCardContent-description-title').text.strip()
                                except Exception:
                                    try:
                                        title = job.find_element(By.CSS_SELECTOR, 'h2, h3, .title, .job-title').text.strip()
                                    except Exception:
                                        title = 'No encontrado'
                                print(f"[INFOJOBS] Título extraído: {title}")
                            except Exception:
                                title = 'No encontrado'
                                print(f"[INFOJOBS] Título NO encontrado")

                            try:
                                company = job.find_element(By.CSS_SELECTOR, '.ij-OfferCardContent-description-subtitle').text.strip()
                            except Exception:
                                try:
                                    company = job.find_element(By.CSS_SELECTOR, '.company, .empresa, .subtitle').text.strip()
                                except Exception:
                                    company = 'Sin empresa'
                            print(f"[INFOJOBS] Empresa extraída: {company}")

                            try:
                                location = job.find_element(By.CSS_SELECTOR, '.ij-OfferCardContent-description-location').text.strip()
                            except Exception:
                                try:
                                    location = job.find_element(By.CSS_SELECTOR, '.location, .ubicacion').text.strip()
                                except Exception:
                                    location = 'España'
                            print(f"[INFOJOBS] Ubicación extraída: {location}")

                            # Intentar obtener el enlace y descripción con logs y selectores alternativos
                            try:
                                link = job.find_element(By.CSS_SELECTOR, '.ij-OfferCardContent-description-title-link').get_attribute('href')
                            except Exception:
                                try:
                                    link = job.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
                                except Exception:
                                    link = None
                            print(f"[INFOJOBS] Link extraído: {link}")

                            description = ''
                            if link:
                                try:
                                    driver.execute_script(f"window.open('{link}', '_blank');")
                                    self.random_sleep(1, 2)
                                    driver.switch_to.window(driver.window_handles[-1])
                                    try:
                                        WebDriverWait(driver, 10).until(
                                            EC.presence_of_element_located((By.CSS_SELECTOR, '.ij-OfferDetail-description, .description, .job-description, .oferta-description'))
                                        )
                                        description = driver.find_element(By.CSS_SELECTOR, '.ij-OfferDetail-description, .description, .job-description, .oferta-description').text.strip()
                                    except Exception:
                                        description = ''
                                    driver.close()
                                    driver.switch_to.window(driver.window_handles[0])
                                except Exception:
                                    description = ''
                            print(f"[INFOJOBS] Descripción extraída: {description[:100]}...")

                            # Añadir la oferta a la lista
                            jobs.append({
                                'titulo': title,
                                'empresa': company,
                                'ubicacion': location,
                                'fecha_publicacion': datetime.now().strftime("%Y-%m-%d"),
                                'portal': 'InfoJobs',
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
