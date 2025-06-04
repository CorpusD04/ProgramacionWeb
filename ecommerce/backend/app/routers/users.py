# Importación de módulos necesarios
from fastapi import APIRouter, Depends  # FastAPI para definir rutas y manejar dependencias
from sqlalchemy.orm import Session  # SQLAlchemy para manejar sesiones de base de datos
from app.database import SessionLocal  # Función para obtener la conexión con la base de datos
from app.database import get_db  # Función para obtener la sesión de la base de datos
from app.models import User  # Modelo de la base de datos para usuarios
from app.auth import hash_password, create_access_token, verify_password  # Funciones de autenticación y seguridad

# Creación del router para manejar rutas relacionadas con usuarios
router = APIRouter(prefix="/users", tags=["Usuarios"])

# Función generadora para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()  # Obtiene una nueva sesión de la base de datos
    try:
        yield db  # Se retorna la sesión activa
    finally:
        db.close()  # Se cierra la sesión al finalizar

# Endpoint para registrar nuevos usuarios en la base de datos
@router.post("/register")
def register_user(username: str, password: str, db: Session = Depends(get_db)):  # Recibe nombre de usuario y contraseña como parámetros
    hashed_password = hash_password(password)  # Se aplica hashing a la contraseña para almacenarla de manera segura
    new_user = User(username=username, password=hashed_password)  # Crea un nuevo usuario con los datos proporcionados
    db.add(new_user)  # Se agrega el usuario a la sesión de la base de datos
    db.commit()  # Se confirman los cambios en la base de datos
    return {"message": "Usuario registrado correctamente"}  # Retorna mensaje de éxito

# Endpoint para iniciar sesión y generar un token de autenticación
@router.post("/login")
def login_user(username: str, password: str, db: Session = Depends(get_db)):  # Recibe credenciales del usuario
    user = db.query(User).filter(User.username == username).first()  # Busca el usuario en la base de datos
    if not user or not verify_password(password, user.password):  # Verifica si el usuario existe y si la contraseña es correcta
        return {"error": "Credenciales incorrectas"}  # Retorna mensaje de error si las credenciales no coinciden
    
    token = create_access_token({"sub": user.username})  # Genera un token de acceso para el usuario autenticado
    return {"access_token": token, "token_type": "bearer"}  # Retorna el token de autenticación y su tipo
