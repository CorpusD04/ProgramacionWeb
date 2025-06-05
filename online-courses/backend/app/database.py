# Importa los módulos necesarios de SQLAlchemy y dotenv
from sqlalchemy import create_engine  # Crea la conexión con la base de datos
from sqlalchemy.orm import sessionmaker, declarative_base, Session  # Manejo de sesiones y declaración de modelos
from dotenv import load_dotenv  # Carga las variables de entorno desde un archivo `.env`
import os  # Permite el acceso a las variables del sistema

# Cargar variables de entorno
load_dotenv()  # Carga las variables definidas en el archivo `.env`

# Define la URL de la base de datos (cambiar según el entorno)
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:fairy15@localhost:3307/onlinecourse"

# Crea el motor de conexión con la base de datos usando la URL definida
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Configura la sesión de SQLAlchemy
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  
# `autocommit=False`: Las transacciones no se confirman automáticamente
# `autoflush=False`: Evita la escritura automática de cambios en la base de datos

# Define la base para la creación de modelos en SQLAlchemy
Base = declarative_base()

# Función para crear las tablas de la base de datos automáticamente (ejecutar una vez)
def init_db():
    import app.models  # Importa los modelos de la aplicación
    Base.metadata.create_all(bind=engine)  # Crea las tablas según los modelos definidos

# Función `get_db` para manejar la sesión de la base de datos
def get_db():
    db = SessionLocal()  # Crea una nueva sesión
    try:
        yield db  # Retorna la sesión para su uso en las operaciones de la base de datos
    finally:
        db.close()  # Cierra la sesión al terminar
