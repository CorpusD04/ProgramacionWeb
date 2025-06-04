# Importación de módulos necesarios
from fastapi import FastAPI  # Framework FastAPI para construir la API
from app.routers import products, users, orders  # Importación de routers para manejar diferentes recursos
from app.auth import router as auth_router  # Importación del router de autenticación
from app.database import engine, Base  # Importación del motor de base de datos y la clase base para modelos
from fastapi.middleware.cors import CORSMiddleware  # Middleware para manejar CORS en la API

# Creación de la instancia de la aplicación FastAPI
app = FastAPI()

# Configuración del middleware CORS para permitir solicitudes desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite solicitudes desde cualquier origen
    allow_credentials=True,  # Permite el uso de credenciales en las solicitudes
    allow_methods=["*"],  # Permite cualquier método HTTP (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permite cualquier encabezado en las solicitudes
)

# Creación de las tablas en la base de datos a partir de los modelos definidos
Base.metadata.create_all(bind=engine)  # Se ejecuta una creación automática de tablas en MySQL

# Inclusión de los routers en la aplicación para manejar las rutas de productos, usuarios, pedidos y autenticación
app.include_router(products.router)  # Agrega las rutas relacionadas con productos
app.include_router(users.router)  # Agrega las rutas relacionadas con usuarios
app.include_router(orders.router)  # Agrega las rutas relacionadas con pedidos
app.include_router(auth_router)  # Agrega las rutas relacionadas con autenticación

# Endpoint de bienvenida en la raíz de la API
@app.get("/")
def home():
    return {"message": "Bienvenido a la API de Ecommerce"}  # Respuesta de bienvenida para indicar que la API está funcionando correctamente