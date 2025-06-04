# Importación de módulos necesarios
import requests  # Librería para hacer solicitudes HTTP
from fastapi import APIRouter, Depends  # FastAPI para definir rutas y manejar dependencias
from sqlalchemy.orm import Session  # SQLAlchemy para manejar sesiones de base de datos
from app.database import SessionLocal  # Función para obtener la conexión a la base de datos
from app.models import Product  # Modelo de la base de datos para productos

# Definición de la API externa de productos falsos
FAKESTORE_API = "https://fakestoreapi.com/products"

# Creación del router para manejar rutas relacionadas con productos
router = APIRouter(prefix="/products", tags=["Productos"])

# Función generadora para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()  # Se obtiene la sesión de la base de datos
    try:
        yield db  # Se retorna la sesión
    finally:
        db.close()  # Se cierra la sesión al finalizar

# Endpoint para obtener todos los productos desde la base de datos
@router.get("/")
def get_all_products(db: Session = Depends(get_db)):  # Se usa una dependencia para obtener la sesión de la base de datos
    products = db.query(Product).all()  # Consulta todos los productos en la base de datos
    return [{"id": p.id, "title": p.name, "image": p.image, "price": p.price} for p in products]  # Retorna los productos en formato JSON

# Función para obtener productos desde la API externa y almacenarlos en la base de datos
def fetch_and_store_products():
    db = SessionLocal()  # Obtiene una nueva sesión de la base de datos
    
    response = requests.get(FAKESTORE_API)  # Solicita los productos a la API externa
    products = response.json()  # Convierte la respuesta a formato JSON
    
    for product in products:  # Itera sobre los productos obtenidos
        existing_product = db.query(Product).filter(Product.name == product["title"]).first()  # Busca si el producto ya existe en la base de datos
        if not existing_product:  # Verifica si el producto no está registrado (para evitar duplicados)
            new_product = Product(
                name=product["title"],  # Nombre del producto
                price=product["price"],  # Precio del producto
                stock=10,  # Stock inicial predefinido
                image=product["image"]  # URL de la imagen del producto
            )
            db.add(new_product)  # Agrega el producto a la sesión

    db.commit()  # Confirma los cambios en la base de datos
    db.close()  # Cierra la sesión de la base de datos

# Llamada a la función para obtener y almacenar productos al iniciar el código
fetch_and_store_products()