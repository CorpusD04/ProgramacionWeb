# Importa módulos necesarios
import os  # Manejo de variables de entorno y configuración del sistema
import requests  # Librería para realizar solicitudes HTTP
from fastapi import APIRouter, HTTPException, Query  # FastAPI para definir rutas y manejar excepciones
from dotenv import load_dotenv  # Librería para cargar variables de entorno desde un archivo .env

# Cargar variables de entorno
load_dotenv()  # Carga las variables de entorno desde un archivo .env
UDEMY_API_URL = "https://www.udemy.com/api-2.0/courses/"  # URL base de la API de Udemy
UDEMY_API_KEY = os.getenv("UDEMY_API_KEY")  # Obtiene la clave de API de Udemy desde las variables de entorno

# Configurar router para manejar rutas relacionadas con cursos externos
router = APIRouter(prefix="/external-courses", tags=["Cursos Externos"])

# Función para obtener cursos de Udemy con paginación y filtros
def fetch_udemy_courses(category: str = None, page: int = 1, page_size: int = 10):
    headers = {"Authorization": f"Bearer {UDEMY_API_KEY}"}  # Agrega la clave de API en los encabezados de la solicitud
    params = {"page": page, "page_size": page_size}  # Configura los parámetros de paginación

    if category:
        params["category"] = category  # Filtra los cursos por categoría si se especifica

    try:
        # Realiza una solicitud GET a la API de Udemy con los parámetros definidos
        response = requests.get(UDEMY_API_URL, headers=headers, params=params)
        response.raise_for_status()  # Maneja errores HTTP y lanza una excepción en caso de fallo

        # Convierte la respuesta en formato JSON
        data = response.json()
        # Extrae la información relevante de cada curso
        courses = [
            {
                "name": c["title"],  # Título del curso
                "provider": "Udemy",  # Plataforma de origen
                "url": f"https://www.udemy.com/course/{c['id']}"  # URL del curso
            }
            for c in data.get("results", [])
        ]
        return {"total_courses": data.get("count", 0), "courses": courses}  # Retorna los cursos obtenidos

    except requests.exceptions.RequestException as e:
        # Lanza una excepción si ocurre un error al conectar con la API de Udemy
        raise HTTPException(status_code=500, detail=f"Error al conectar con Udemy: {str(e)}")

# Endpoint para obtener cursos de Udemy con filtros y paginación
@router.get("/")
def get_external_courses(
    category: str = Query(None, title="Filtrar por categoría"),  # Permite filtrar cursos por categoría
    page: int = Query(1, title="Número de página", ge=1),  # Define el número de página con un valor mínimo de 1
    page_size: int = Query(10, title="Cantidad de cursos por página", ge=1, le=100)  # Define el tamaño de la página con límites
):
    return fetch_udemy_courses(category, page, page_size)  # Llama a la función fetch_udemy_courses con los parámetros recibidos
