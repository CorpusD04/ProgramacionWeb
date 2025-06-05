# Importa los módulos necesarios de SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, Boolean  # Define tipos de columnas y relaciones
from sqlalchemy.orm import relationship  # Maneja relaciones entre tablas
from app.database import Base  # Importa la base de datos definida en la aplicación

# Definición de la tabla de usuarios en la base de datos
class User(Base):
    __tablename__ = "users"  # Nombre de la tabla en la base de datos

    id = Column(Integer, primary_key=True, index=True)  # ID único para cada usuario
    name = Column(String(100), nullable=False)  # Nombre del usuario (máximo 100 caracteres)
    email = Column(String(100), unique=True, nullable=False)  # Email único (máximo 100 caracteres)
    password = Column(String(255), nullable=False)  # Contraseña encriptada del usuario

    courses = relationship("UserCourse", back_populates="user")  # Relación con cursos inscritos por el usuario

# Definición de la tabla de cursos en la base de datos
class Course(Base):
    __tablename__ = "courses"  # Nombre de la tabla en la base de datos

    id = Column(Integer, primary_key=True, index=True)  # ID único del curso
    title = Column(String(255))  # Título del curso
    description = Column(Text)  # Descripción detallada del curso
    category = Column(String(100))  # Categoría a la que pertenece el curso
    url = Column(String(255))  # Enlace externo al curso (Udemy, Coursera, YouTube, etc.)
    provider = Column(String(100))  # Plataforma que ofrece el curso (YouTube, Coursera, etc.)
    image = Column(String(255))  # URL de una imagen opcional asociada al curso

# Definición de la tabla intermedia que relaciona usuarios con cursos inscritos
class UserCourse(Base):
    __tablename__ = "user_courses"  # Nombre de la tabla en la base de datos

    id = Column(Integer, primary_key=True, index=True)  # ID único de la inscripción
    user_id = Column(Integer, ForeignKey("users.id"))  # ID del usuario inscrito en el curso
    course_id = Column(Integer, ForeignKey("courses.id"))  # ID del curso al que está inscrito el usuario
    completed = Column(Boolean, default=False)  # Indica si el usuario completó el curso (False por defecto)

    user = relationship("User", back_populates="courses")  # Relación con la tabla de usuarios
    course = relationship("Course")  # Relación con la tabla de cursos
