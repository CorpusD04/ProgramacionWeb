# Importa FastAPI para crear la aplicación web
from fastapi import FastAPI  

# Importa los módulos de rutas que contienen la lógica de los usuarios, cursos, progreso y proveedores
from app.routers import users, courses, progress, providers  

# Importa la función para inicializar la base de datos
from app.database import init_db  

# Importa el middleware CORS para permitir solicitudes desde el frontend
from fastapi.middleware.cors import CORSMiddleware  

# Crea la instancia de la aplicación FastAPI
app = FastAPI()  

# Configuración de CORS para permitir el acceso desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # ✅ Permite solicitudes desde el frontend en el puerto 3000
    allow_credentials=True,  # ✅ Permite el uso de cookies y autenticación en solicitudes
    allow_methods=["*"],  # ✅ Permite todos los métodos HTTP (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # ✅ Permite todos los encabezados en las solicitudes
)

# Inicializa la base de datos al iniciar la aplicación
init_db()  

# Incluye las rutas en la aplicación para manejar las distintas funcionalidades
app.include_router(users.router)  # Rutas para gestión de usuarios
app.include_router(courses.router)  # Rutas para cursos
app.include_router(progress.router)  # Rutas para progreso del usuario en los cursos
app.include_router(providers.router)  # Rutas para proveedores externos de cursos
