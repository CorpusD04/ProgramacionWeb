# Importación de módulos necesarios para la conexión con la base de datos
from sqlalchemy import create_engine  # Módulo para crear la conexión con la base de datos
from sqlalchemy.orm import sessionmaker  # Módulo para manejar sesiones de base de datos
from sqlalchemy.ext.declarative import declarative_base  # Herramienta para definir modelos ORM

# Definición de la URL de la base de datos con MySQL y PyMySQL
DATABASE_URL = "mysql+pymysql://root:fairy15@localhost:3307/ecommerce"

# Creación del motor de base de datos, que permite la conexión con MySQL
engine = create_engine(DATABASE_URL)

# Configuración de la sesión de la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Creación de la clase base para la declaración de modelos ORM
Base = declarative_base()

# Función generadora para obtener la sesión activa de la base de datos
def get_db():
    db = SessionLocal()  # Inicia una nueva sesión de base de datos
    try:
        yield db  # Retorna la sesión activa para ser utilizada en otros componentes
    finally:
        db.close()  # Cierra la sesión al finalizar
