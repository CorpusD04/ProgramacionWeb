# Importa módulos necesarios para interactuar con APIs y bases de datos
import os  # Manejo de variables de entorno
import requests  # Librería para realizar solicitudes HTTP
from googleapiclient.discovery import build  # Google API Client para acceder a datos de YouTube
from bs4 import BeautifulSoup  # Librería para hacer web scraping
from sqlalchemy.orm import Session  # Manejo de sesiones de base de datos con SQLAlchemy
import sys  # Módulo del sistema para modificar rutas de importación

# Modifica la ruta para poder importar módulos desde la carpeta padre
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Importa configuraciones de la base de datos y el modelo de cursos
from app.database import SessionLocal
from app.models import Course

# 🔹 API key de YouTube desde variables de entorno
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")  # Carga la clave desde el archivo .env

# 🔹 Función para obtener cursos de YouTube desde un canal específico
def fetch_youtube_courses(channel_id, max_results=10):
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)  # Inicializa la API de YouTube
    response = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        maxResults=max_results,
        type="video"
    ).execute()  # Realiza la consulta a la API

    courses = []
    for item in response.get("items", []):
        snippet = item["snippet"]
        courses.append({
            "title": snippet["title"],  # Título del video/curso
            "description": snippet.get("description", ""),  # Descripción opcional
            "provider": "YouTube",  # Plataforma de origen
            "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}",  # URL del curso
            "category": "programación",  # Categoría fija (puedes hacerla dinámica)
            "image": snippet.get("thumbnails", {}).get("high", {}).get("url", "")  # Imagen del curso
        })
    return courses  # Retorna la lista de cursos obtenidos

# 🔹 Función para obtener cursos de FreeCodeCamp mediante web scraping
def fetch_freecodecamp_courses():
    url = "https://www.freecodecamp.org/news/tag/courses/"
    response = requests.get(url)  # Hace una petición HTTP para obtener el contenido de la página
    soup = BeautifulSoup(response.text, "html.parser")  # Analiza el HTML con BeautifulSoup

    courses = []
    for article in soup.find_all("article"):  # Recorre los artículos de la página
        title_tag = article.find("h2")  # Extrae el título del curso
        link_tag = article.find("a")  # Extrae el enlace al curso
        if title_tag and link_tag:  # Verifica que ambos elementos existan
            courses.append({
                "title": title_tag.text.strip(),  # Obtiene y limpia el título del curso
                "description": "",  # No hay descripción disponible en la página
                "provider": "FreeCodeCamp",  # Plataforma de origen
                "url": link_tag["href"],  # URL del curso
                "category": "desarrollo web",  # Categoría fija (puedes hacerla dinámica)
                "image": ""  # No hay imágenes disponibles
            })
    return courses  # Retorna la lista de cursos obtenidos

# 🔹 Función para insertar cursos en la base de datos si aún no existen
def insert_courses_to_db(courses):
    db: Session = SessionLocal()  # Inicia una sesión en la base de datos
    inserted = 0  # Contador de cursos insertados

    for course in courses:
        exists = db.query(Course).filter(Course.url == course["url"]).first()  # Verifica si el curso ya existe en la DB
        if not exists:
            new_course = Course(**course)  # Crea una nueva entrada de curso
            db.add(new_course)  # Agrega el curso a la sesión
            inserted += 1  # Incrementa el contador de cursos insertados

    db.commit()  # Guarda los cambios en la base de datos
    db.close()  # Cierra la sesión
    return inserted  # Retorna el número de cursos insertados

# 🔹 Función principal que ejecuta el proceso de extracción e inserción de cursos
def main():
    youtube_channel_id = "UC8butISFwT-Wl7EV0hUK0BQ"  # ID del canal FreeCodeCamp en YouTube
    yt_courses = fetch_youtube_courses(youtube_channel_id)  # Obtiene cursos de YouTube
    fcc_courses = fetch_freecodecamp_courses()  # Obtiene cursos de FreeCodeCamp

    all_courses = yt_courses + fcc_courses  # Combina los cursos obtenidos
    total_inserted = insert_courses_to_db(all_courses)  # Inserta los cursos en la base de datos

    print(f"✅ Se insertaron {total_inserted} cursos nuevos.")  # Muestra un mensaje de éxito

# 🔹 Ejecuta la función principal si el script es ejecutado directamente
if __name__ == "__main__":
    main()
