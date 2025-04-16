import requests
from bs4 import BeautifulSoup
from scraping.models import OfertaEmpleo

def scrap_infojobs(keyword="python"):
    print("📡 Conectando con InfoJobs...")

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    url = f"https://www.infojobs.net/jobsearch/search-results/list.xhtml?keyword={keyword}"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"❌ Error al conectar: {response.status_code}")
        return

    soup = BeautifulSoup(response.content, "html.parser")

    ofertas = soup.select("li[class*='element']")

    if not ofertas:
        print("⚠️ No se encontraron ofertas. Ajusta el selector.")
        return

    for oferta in ofertas:
        titulo = oferta.select_one("h2 h3")
        empresa = oferta.select_one(".list-element-company")
        link = oferta.select_one("a")

        if titulo and empresa and link:
            titulo_text = titulo.get_text(strip=True)
            empresa_text = empresa.get_text(strip=True)
            link_url = link['href']

            print(f"🟢 {titulo_text} - {empresa_text}")

            OfertaEmpleo.objects.get_or_create(
                titulo=titulo_text,
                empresa=empresa_text,
                ubicacion="Desconocida",
                fecha_publicacion=None,
                plataforma="InfoJobs",
                url=link_url
            )

    print("✅ Scraping completado con éxito.")
