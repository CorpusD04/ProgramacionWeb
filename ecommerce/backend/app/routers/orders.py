# Importación de módulos y dependencias necesarias
from fastapi import APIRouter, Depends, HTTPException, FastAPI  # Importa FastAPI y sus componentes para manejar rutas y excepciones
from sqlalchemy.orm import Session  # Módulo de SQLAlchemy para manejar sesiones de base de datos
from app.database import get_db  # Función para obtener la conexión con la base de datos
from app.models import Order, OrderItem  # Modelos de la base de datos relacionados con pedidos y elementos del pedido
from app.schemas import OrderCreate  # Esquema utilizado para la creación de pedidos
from app.auth import get_current_user  # Función para obtener información del usuario autenticado
from app.routers import products, users, orders  # Importación de routers relacionados
from sqlalchemy.orm import joinedload  # Utilidad de SQLAlchemy para realizar carga conjunta de relaciones

# Creación del router para manejar rutas de pedidos
router = APIRouter(prefix="/orders", tags=["Pedidos"])

# Creación de la instancia de la aplicación FastAPI
app = FastAPI()

# Registro del router de pedidos en la aplicación
app.include_router(orders.router)  

# Definición de endpoint para obtener todos los pedidos
@router.get("/")
def get_orders(db: Session = Depends(get_db)):  # Dependencia para obtener la sesión de la base de datos
    orders = db.query(Order).options(joinedload(Order.order_items)).all()  # Consulta todos los pedidos y carga los productos asociados

    # Serialización de pedidos con sus elementos de pedido
    results = []
    for order in orders:
        results.append({
            "id": order.id,  # ID del pedido
            "user_id": order.user_id,  # ID del usuario que realizó el pedido
            "total": order.total,  # Total del pedido
            "status": order.status,  # Estado del pedido
            "order_items": [  # Lista de productos del pedido
                {
                    "id": item.id,  # ID del producto en el pedido
                    "product_id": item.product_id,  # ID del producto
                    "title": item.title,  # Título del producto
                    "image": item.image,  # URL de la imagen del producto
                    "quantity": item.quantity,  # Cantidad adquirida del producto
                    "price": item.price,  # Precio unitario del producto
                    "status": order.status  # Estado del pedido
                }
                for item in order.order_items  # Iteración sobre los productos del pedido
            ]
        })

    return results  # Retorna los pedidos con los elementos asociados


# Definición de endpoint para la creación de pedidos
@router.post("/")
def create_order(order_data: OrderCreate, db: Session = Depends(get_db)):  # Recibe datos del pedido en formato OrderCreate
    print("Datos recibidos en el backend:", order_data.dict())  # Registro de datos en consola para depuración
    
    if not order_data.user_id:
        raise HTTPException(status_code=401, detail="Usuario no autenticado")  # Lanza excepción si no hay usuario autenticado

    # Creación del objeto pedido en la base de datos
    new_order = Order(user_id=order_data.user_id, total=order_data.total, status="Pendiente")
    db.add(new_order)  # Se agrega el pedido a la sesión
    db.commit()  # Se confirma la inserción en la base de datos
    db.refresh(new_order)  # Se actualiza el objeto con datos de la base

    # Iteración sobre los productos dentro del pedido
    for item in order_data.items:
        order_item = OrderItem(
            order_id=new_order.id,  # Asociado al nuevo pedido
            product_id=item.product_id,  # ID del producto
            title=item.title,  # Título del producto
            image=item.image,  # Imagen del producto
            quantity=item.quantity,  # Cantidad
            price=item.price,  # Precio unitario
            status="Pendiente"  # Estado inicial del producto en el pedido
        )
        db.add(order_item)  # Se agrega el producto a la sesión de la base de datos

    db.commit()  # Se confirma la inserción de los productos
    print(f"Pedido registrado con éxito, ID: {new_order.id}")  # Mensaje de confirmación en consola
    return {"message": "Pedido registrado con éxito", "order_id": new_order.id}  # Retorno de mensaje de éxito


# Endpoint para eliminar un producto específico del pedido
@router.delete("/item/{item_id}")
def delete_order_item(item_id: int, db: Session = Depends(get_db)):  # Recibe el ID del producto a eliminar
    order_item = db.query(OrderItem).filter(OrderItem.id == item_id).first()  # Busca el producto en la base de datos

    if not order_item:
        raise HTTPException(status_code=404, detail="El producto del pedido no fue encontrado.")  # Lanza error si no se encuentra

    db.delete(order_item)  # Elimina el producto
    db.commit()  # Confirma la eliminación en la base de datos

    return {"message": "Producto del pedido eliminado exitosamente"}  # Retorna mensaje de éxito


# Endpoint para simular el pago de un producto
@router.post("/pay/{item_id}")
def pay_item(item_id: int, db: Session = Depends(get_db)):  # Recibe el ID del producto a pagar
    item = db.query(OrderItem).filter(OrderItem.id == item_id).first()  # Consulta el producto en el pedido
    if not item:
        raise HTTPException(status_code=404, detail="Producto no encontrado en pedido")  # Lanza excepción si no existe

    order = db.query(Order).filter(Order.id == item.order_id).first()  # Consulta el pedido asociado
    if not order:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")  # Lanza error si no existe

    # Actualiza el estado del pedido
    order.status = "Pagado"
    db.commit()  # Confirma el cambio en la base de datos

    return {"message": "Pedido pagado correctamente"}  # Retorna mensaje de éxito