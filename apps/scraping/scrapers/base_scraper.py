import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException

class BaseScraper:
    def __init__(self, headless=True):
        self.headless = headless
        self.driver = None

    def get_driver(self):
        """Configurar y retornar un driver de Chrome"""
        if self.driver is not None:
            try:
                self.driver.quit()
            except:
                pass
        
        try:
            options = Options()
            if self.headless:
                options.add_argument('--headless=new')
                
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--window-size=1920,1080')
            
            # Configurar el user agent
            options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
            
            # Usar Selenium con ChromeDriver
            self.driver = webdriver.Chrome(options=options)
            
            # Configurar el tamaño de la ventana
            self.driver.set_window_size(1920, 1080)
            
            return self.driver
            
        except WebDriverException as e:
            print(f"Error al inicializar el driver: {str(e)}")
            return None

    def random_sleep(self, min_seconds=1, max_seconds=3):
        """Esperar un tiempo aleatorio entre min_seconds y max_seconds"""
        time.sleep(random.uniform(min_seconds, max_seconds))

    def close(self):
        """Cerrar recursos si es necesario"""
        if self.driver is not None:
            try:
                self.driver.quit()
            except:
                pass
            self.driver = None