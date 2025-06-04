from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Product(Base):  # Tabla productos
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True) # Id del producto 
    name = Column(String(100), index=True) # Nombre del producto 
    price = Column(Float) # Precio del producto 
    stock = Column(Integer) # Almacenamiento disponible
    image = Column(String(255))  # Guardar la URL de la imagen

class User(Base): #Tabla Usuarios
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)  #Id del usuario
    username = Column(String(50), unique=True, index=True) # Nombre del usuario
    email = Column(String(100), unique=True, index=True) # email del usuario
    password = Column(String(255)) # Contraseña del usuario
    region = Column(String(100)) # Region del usuario
    address = Column(String(255)) # Direccion del usuario

class Order(Base):  
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)  # ID del pedido
    user_id = Column(Integer, ForeignKey("users.id"))  # ID del usuario que realizó el pedido
    total = Column(Float)  # Total de la compra del usuario
    status = Column(String(50), default="Pendiente")  # Estado del pedido (Pendiente/Pagado)
    user = relationship("User")  # Relación con la tabla de usuarios
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")  # Relación con los productos del pedido

class OrderItem(Base):  
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)  # ID del producto dentro del pedido
    order_id = Column(Integer, ForeignKey("orders.id"))  # Relación con el pedido
    product_id = Column(Integer, ForeignKey("products.id"))  # Relación con la tabla de productos
    title = Column(String(255))  # Nombre del producto
    image = Column(String(255))  # URL de la imagen
    quantity = Column(Integer)  # Cantidad de productos
    price = Column(Float)  # Precio total del producto
    status = Column(String(50), default="Pendiente") 
    order = relationship("Order", back_populates="order_items")  # Relación con pedidos
