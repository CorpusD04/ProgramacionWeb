# Importa módulos necesarios para autenticación y manejo de datos
import os  # Manejo de variables de entorno
import jwt  # Librería para generar y validar JWT
import logging  # Manejo de logs para registrar eventos
from datetime import datetime, timedelta  # Manejo de fechas para expirar tokens
from fastapi import APIRouter, Depends, HTTPException  # FastAPI para definir rutas y manejar dependencias
from sqlalchemy.orm import Session  # SQLAlchemy para trabajar con la base de datos
from dotenv import load_dotenv  # Carga variables de entorno desde un archivo `.env`
from passlib.context import CryptContext  # Librería para manejar la encriptación de contraseñas
from app.database import get_db  # Función para obtener la sesión de la base de datos
from app.models import User  # Modelo de usuario
from app.schemas import UserCreate  # Esquema para la creación de usuarios
from fastapi.security import OAuth2PasswordBearer  # Seguridad OAuth2 para autenticación
from jose import JWTError, jwt  # Librería para manejar JWT en FastAPI

# Configurar logs para registrar eventos del sistema
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()  # Carga las variables desde el archivo `.env`
SECRET_KEY = os.getenv("SECRET_KEY")  # Clave secreta para firmar JWT
ALGORITHM = "HS256"  # Algoritmo utilizado para encriptación
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))  # Duración del token en minutos
print("Clave cargada:", SECRET_KEY)  # ✅ Verifica que la clave se cargó correctamente

# Configurar el enrutador con el prefijo "/auth" y la etiqueta "Autenticación"
router = APIRouter(prefix="/auth", tags=["Autenticación"])

# Configurar el contexto de encriptación para manejar contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Función para generar un JWT de autenticación
def create_access_token(data: dict):
    to_encode = data.copy()  # Copia los datos a codificar en el token
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)  # Define la expiración del token
    to_encode.update({"exp": expire})  # Agrega la fecha de expiración al token
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  # Retorna el token codificado

# Ruta para registrar usuarios en la base de datos
@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()  # Busca si el email ya está registrado
    if existing_user:
        logger.warning(f"Intento de registro con email duplicado: {user.email}")  # Registra un intento fallido en los logs
        raise HTTPException(status_code=400, detail="El correo ya está registrado")  # Retorna un error si el email existe

    hashed_password = pwd_context.hash(user.password)  # Encripta la contraseña
    new_user = User(name=user.name, email=user.email, password=hashed_password)  # Crea el nuevo usuario
    db.add(new_user)  # Agrega el usuario a la base de datos
    db.commit()  # Guarda los cambios
    db.refresh(new_user)  # Refresca la instancia del usuario

    logger.info(f"Usuario registrado correctamente: {user.email}")  # Registra el éxito del registro
    return {"message": "Registro exitoso", "user_id": new_user.id}  # Retorna la respuesta de éxito

# Ruta para iniciar sesión y generar un token JWT
@router.post("/login")
def login_user(user_data: dict, db: Session = Depends(get_db)):  # ✅ Cambia los parámetros
    email = user_data.get("email")  # Obtiene el email del usuario
    password = user_data.get("password")  # Obtiene la contraseña

    if not email or not password:
        raise HTTPException(status_code=400, detail="Se requieren email y contraseña")  # Retorna error si falta información

    user = db.query(User).filter(User.email == email).first()  # Busca el usuario en la base de datos
    if not user or not pwd_context.verify(password, user.password):  # Verifica la contraseña
        raise HTTPException(status_code=401, detail="Credenciales inválidas")  # Retorna error si no es válido

    return {"message": "Inicio de sesión exitoso", "user_id": user.id}  # Retorna éxito si la autenticación es correcta

# Configurar OAuth2 para manejar autenticación basada en tokens
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Función para obtener el usuario actual autenticado a través de JWT
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])  # Decodifica el token
        user_id: int = payload.get("user_id")  # Obtiene el ID del usuario desde el token
        if user_id is None:  # Verifica que el ID sea válido
            raise HTTPException(status_code=401, detail="Token inválido")  # Retorna error si el token no tiene usuario
        user = db.query(User).filter(User.id == user_id).first()  # Busca el usuario en la base de datos
        if user is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")  # Retorna error si el usuario no existe
        return user  # Retorna el usuario autenticado
    except JWTError:  # Manejo de errores de JWT
        raise HTTPException(status_code=401, detail="Token inválido")  # Retorna error si el token no es válido

# Ruta para cerrar sesión (solo se elimina el token en el frontend)
@router.post("/logout")
def logout():
    return {"message": "Sesión cerrada"}  # Retorna mensaje de éxito en el cierre de sesión
