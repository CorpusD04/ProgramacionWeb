# Importación de módulos necesarios
from fastapi import APIRouter, Depends, HTTPException  # FastAPI para manejar rutas, dependencias y excepciones
from sqlalchemy.orm import Session  # SQLAlchemy para gestionar sesiones de base de datos
from app.database import get_db  # Función para obtener la sesión de la base de datos
from app.models import User  # Modelo de la base de datos para usuarios
from passlib.context import CryptContext  # Biblioteca para manejar el hash de contraseñas
from datetime import datetime, timedelta  # Módulo para manejar fechas y tiempos
from jose import JWTError, jwt  # Biblioteca para generar y decodificar tokens JWT
from pydantic import BaseModel  # Modelo de datos con validaciones
from fastapi.security import OAuth2PasswordBearer  # Esquema de autenticación basado en OAuth2

# Configuración del esquema de autenticación con OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Creación del router para las rutas de autenticación
router = APIRouter(prefix="/auth", tags=["Autenticación"])

# Configuración del contexto de hash de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Definición de claves y parámetros para el manejo de JWT
SECRET_KEY = "tu_clave_secreta"  # Clave secreta para firmar los tokens JWT
ALGORITHM = "HS256"  # Algoritmo utilizado para cifrado del JWT
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Tiempo de expiración del token en minutos

# Función para obtener el usuario actual a partir del token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  # Decodifica el token JWT
        user_id: int = payload.get("user_id")  # Extrae el ID del usuario del payload

        if user_id is None:  # Verifica si el ID está presente
            raise HTTPException(status_code=401, detail="Token inválido")

        user = db.query(User).filter(User.id == user_id).first()  # Consulta el usuario en la base de datos

        if user is None:  # Verifica si el usuario existe
            raise HTTPException(status_code=401, detail="Usuario no encontrado")

        return user  # Retorna el usuario autenticado
    except JWTError:  # Manejo de errores en la validación del token JWT
        raise HTTPException(status_code=401, detail="Token inválido")

# Función para generar un token de acceso JWT
def create_access_token(data: dict):
    to_encode = data.copy()  # Copia los datos proporcionados
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)  # Calcula el tiempo de expiración
    to_encode.update({"exp": expire})  # Agrega la expiración al payload
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  # Genera el token JWT
    return encoded_jwt  # Retorna el token generado

# Función para hashear una contraseña utilizando bcrypt
def hash_password(password: str):
    return pwd_context.hash(password)  # Devuelve la contraseña encriptada

# Modelo de datos para la creación de usuarios
class UserCreate(BaseModel):
    username: str  # Nombre de usuario
    email: str  # Correo electrónico
    password: str  # Contraseña
    region: str  # Región del usuario
    address: str  # Dirección del usuario

# Endpoint para el registro de nuevos usuarios
@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):  # Recibe un modelo de usuario y una sesión de BD
    existing_user = db.query(User).filter(User.email == user.email).first()  # Verifica si el correo ya está registrado
    if existing_user:  # Si el usuario ya existe, retorna una excepción
        raise HTTPException(status_code=400, detail="El correo ya está registrado.")
    
    new_user = User(
        username=user.username,  # Nombre del usuario
        email=user.email,  # Correo electrónico
        password=hash_password(user.password),  # Hashea la contraseña antes de almacenarla
        region=user.region,  # Región del usuario
        address=user.address  # Dirección del usuario
    )

    db.add(new_user)  # Agrega el usuario a la base de datos
    db.commit()  # Confirma los cambios en la base de datos
    return {"message": "Registro exitoso"}  # Retorna un mensaje de éxito

# Modelo de datos para el inicio de sesión de usuarios
class UserLogin(BaseModel):
    email: str  # Correo electrónico
    password: str  # Contraseña

# Función para verificar una contraseña comparándola con su hash almacenado
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)  # Verifica si la contraseña es válida

# Endpoint para iniciar sesión y generar un token de autenticación
@router.post("/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):  # Recibe las credenciales del usuario
    db_user = db.query(User).filter(User.email == user.email).first()  # Busca el usuario en la base de datos
    if not db_user or not verify_password(user.password, db_user.password):  # Verifica si la contraseña es correcta
        raise HTTPException(status_code=401, detail="Credenciales inválidas")  # Retorna un error si las credenciales son incorrectas
    
    access_token = create_access_token({"user_id": db_user.id})  #  Genera un token JWT para el usuario autenticado
    return {"access_token": access_token, "token_type": "bearer", "message": "Inicio de sesión exitoso", "user_id": db_user.id}  # Retorna el token y un mensaje de éxito