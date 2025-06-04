# Importación de módulos necesarios
from pydantic import BaseModel  # Pydantic para definir modelos de datos con validaciones
from typing import List  # Módulo para definir listas de elementos en los modelos

# Definición del modelo para los elementos de un pedido
class OrderItemCreate(BaseModel):
    product_id: int  # ID del producto en el pedido
    title: str  # Nombre del producto
    image: str  # URL de la imagen del producto
    quantity: int  # Cantidad adquirida del producto
    price: float  # Precio unitario del producto

# Definición del modelo para la creación de un pedido
class OrderCreate(BaseModel):
    user_id: int  # ID del usuario que realiza el pedido
    total: float  # Total del pedido
    items: List[OrderItemCreate]  # Lista de productos incluidos en el pedido
