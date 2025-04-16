# apps/inteligencia/normalizador.py

import re
from apps.scraping.models import OfertaEmpleo

# Lista ampliada de tecnologías y stacks modernos (puedes seguir ampliando)
TECNOLOGIAS = [
    # Lenguajes y stacks populares
    "Python", "Java", "JavaScript", "TypeScript", "C#", "C++", "C", "Go", "Ruby", "PHP", "Perl", "Scala", "Swift", "Objective-C", "Kotlin", "Rust", "MATLAB", "R",
    # Frameworks y librerías backend/frontend
    ".NET", "ASP.NET", "Node.js", "Node", "Express", "Next.js", "Nuxt.js", "NestJS", "Svelte", "SvelteKit", "React", "Angular", "Vue", "Flask", "Django", "Spring", "Laravel", "Symfony", "Rails", "Ruby on Rails", "Bootstrap", "jQuery", "Redux", "MobX",
    # Data, ML, Big Data
    "TensorFlow", "PyTorch", "Pandas", "NumPy", "Scikit-learn", "Keras", "Spark", "Hadoop", "Airflow",
    # DevOps, Cloud, CI/CD
    "Docker", "Kubernetes", "AWS", "Azure", "GCP", "Google Cloud", "Heroku", "Firebase", "Jenkins", "Travis", "CircleCI", "GitLab CI", "Bitbucket", "Terraform", "Ansible", "Chef", "Puppet",
    # Bases de datos
    "SQL", "MySQL", "PostgreSQL", "MongoDB", "Redis", "SQLite", "Oracle", "Elasticsearch", "Solr", "Cassandra", "DynamoDB",
    # Otros stacks y herramientas
    "GraphQL", "REST", "SOAP", "RabbitMQ", "Kafka", "Celery", "Jira", "Confluence", "Salesforce", "SAP", "PowerBI", "Tableau", "Qlik", "SAS",
    # Web y diseño
    "HTML", "CSS", "SASS", "LESS", "Tailwind", "Material UI", "Ant Design"
]

# Mejorar regex para detectar palabras, puntos, guiones y signos de suma
TECNOLOGIA_REGEX = re.compile(r'(?<![\w.])(' + '|'.join([re.escape(tec) for tec in TECNOLOGIAS]) + r')(?![\w.])', re.IGNORECASE)

def extraer_tecnologias(descripcion, titulo=None):
    """
    Devuelve una lista de tecnologías detectadas en el texto (descripción y, opcionalmente, título).
    """
    textos = []
    if descripcion:
        textos.append(descripcion)
    if titulo:
        textos.append(titulo)
    if not textos:
        return []
    # Buscar todas las coincidencias
    encontradas = set()
    for texto in textos:
        for match in re.finditer(TECNOLOGIA_REGEX, texto):
            raw = match.group(0)
            for tec in TECNOLOGIAS:
                if raw.lower() == tec.lower():
                    encontradas.add(tec)
                    break
    return sorted(encontradas)

def normalizar_ofertas():
    """
    Recorre todas las ofertas y actualiza el campo 'tecnologias' si es necesario, analizando descripción y título.
    """
    ofertas = OfertaEmpleo.objects.all()
    actualizadas = 0

    for oferta in ofertas:
        tecnologias = extraer_tecnologias(oferta.descripcion, oferta.titulo)
        if tecnologias:
            oferta.tecnologias = ", ".join(tecnologias)
            oferta.save()
            actualizadas += 1

    print(f"✅ Ofertas actualizadas con tecnologías: {actualizadas}")
