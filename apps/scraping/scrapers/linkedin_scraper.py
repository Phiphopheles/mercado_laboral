from .base_scraper import BaseScraper
from datetime import datetime
import urllib.parse
from bs4 import BeautifulSoup
import requests
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LinkedinScraper(BaseScraper):
    def __init__(self, headless=True):
        super().__init__(headless)
        self.base_url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
        self.search_terms = [
            'python developer',
            'javascript developer',
            'java developer',
            'web developer',
            'full stack developer',
            'devops engineer',
            'data engineer'
        ]
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://www.linkedin.com/jobs',
            'Origin': 'https://www.linkedin.com'
        }

    def scrape(self):
        jobs = []
        driver = self.get_driver()
        if driver is None:
            print("No se pudo inicializar el driver para LinkedIn")
            return jobs

        try:
            for search_term in self.search_terms:
                try:
                    # Construir URL de búsqueda
                    params = {
                        'keywords': search_term,
                        'location': 'España',
                        'trk': 'public_jobs_jobs-search-bar_search-submit',
                        'position': 1,
                        'pageNum': 0,
                        'start': 0
                    }
                    response = requests.get(
                        self.base_url,
                        params=params,
                        headers=self.headers
                    )
                    if response.status_code != 200:
                        print(f"Error accediendo a LinkedIn: {response.status_code}")
                        continue
                    response.encoding = 'utf-8'
                    soup = BeautifulSoup(response.text, 'lxml')
                    self.random_sleep(3, 5)
                    job_cards = soup.select('div.base-card')
                    if not job_cards:
                        print(f"No se encontraron ofertas para: {search_term}")
                        continue
                    print(f"Encontradas {len(job_cards)} ofertas para: {search_term}")
                    # Procesar cada oferta
                    for job in job_cards[:10]:
                        try:
                            # Extraer título
                            try:
                                title = job.select_one('.base-search-card__title, .job-title, h3, h2').get_text(strip=True)
                                if not title:
                                    title = 'No encontrado'
                            except Exception:
                                title = 'No encontrado'
                            print(f"[LINKEDIN] Título extraído: {title}")
                            # Extraer empresa
                            try:
                                company = job.select_one('.base-search-card__subtitle, .company, .empresa').get_text(strip=True)
                                if not company:
                                    company = 'Sin empresa'
                            except Exception:
                                company = 'Sin empresa'
                            print(f"[LINKEDIN] Empresa extraída: {company}")
                            # Extraer ubicación
                            try:
                                location = job.select_one('.job-search-card__location, .location, .ubicacion').get_text(strip=True)
                                if not location:
                                    location = 'España'
                            except Exception:
                                location = 'España'
                            print(f"[LINKEDIN] Ubicación extraída: {location}")
                            # Obtener enlace a la oferta
                            link_elem = job.select_one('a.base-card__full-link')
                            link = link_elem['href'] if link_elem else None
                            print(f"[LINKEDIN] Link extraído: {link}")
                            description = ''
                            if link:
                                try:
                                    driver.execute_script(f"window.open('{link}', '_blank');")
                                    self.random_sleep(2, 3)
                                    driver.switch_to.window(driver.window_handles[-1])
                                    # Hacer click en 'Ver más' si existe
                                    try:
                                        ver_mas = driver.find_element(By.CSS_SELECTOR, '.show-more-less-html__button, .artdeco-button--muted')
                                        if ver_mas.is_displayed():
                                            ver_mas.click()
                                            self.random_sleep(1, 2)
                                    except Exception:
                                        pass  # No hay botón 'Ver más'
                                    # Esperar a que cargue la descripción completa
                                    try:
                                        WebDriverWait(driver, 10).until(
                                            EC.presence_of_element_located((By.CSS_SELECTOR, '.show-more-less-html__markup, .description, .job-description, .oferta-description'))
                                        )
                                        # Concatenar todo el texto de los nodos de descripción
                                        desc_nodes = driver.find_elements(By.CSS_SELECTOR, '.show-more-less-html__markup, .description, .job-description, .oferta-description')
                                        description = '\n'.join([n.text.strip() for n in desc_nodes if n.text.strip()])
                                    except Exception:
                                        description = ''
                                    driver.close()
                                    driver.switch_to.window(driver.window_handles[0])
                                except Exception:
                                    description = ''
                            print(f"[LINKEDIN] Descripción extraída: {description[:200]}...")
                            jobs.append({
                                'titulo': title,
                                'empresa': company,
                                'ubicacion': location,
                                'fecha_publicacion': datetime.now().strftime("%Y-%m-%d"),
                                'portal': 'LinkedIn',
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
        finally:
            self.close()
        return jobs
