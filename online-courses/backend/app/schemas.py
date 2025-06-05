# Importa módulos necesarios de Pydantic para validación de datos
from pydantic import BaseModel  # Base para definir esquemas de datos
from typing import Optional  # Permite manejar valores opcionales en los atributos

# 🔹 Definir esquema para usuarios
class UserBase(BaseModel):
    name: str  # Nombre del usuario
    email: str  # Email del usuario

class UserCreate(UserBase):
    password: str  # ✅ Se agrega el atributo 'password' para el registro del usuario

class User(UserBase):
    id: int  # Identificador único del usuario

    class Config:
        orm_mode = True  # ✅ Permite convertir instancias de SQLAlchemy a modelos Pydantic

# 🔹 Esquema para la salida de cursos con información de progreso
class CourseOut(BaseModel):
    id: int  # Identificador único del curso
    title: str  # Título del curso
    description: str  # Descripción del curso
    completed: bool  # ✅ Indica si el usuario ha completado el curso

# 🔹 Definir esquema para cursos
class CourseBase(BaseModel):
    title: str  # Título del curso
    description: Optional[str]  # Descripción del curso (puede ser opcional)
    category: Optional[str]  # Categoría del curso (opcional)
    url: str  # ✅ URL del curso (enlace externo)
    provider: Optional[str]  # Plataforma del curso (Udemy, Coursera, etc.) opcional
    image: Optional[str]  # URL de imagen asociada al curso (opcional)

class CourseCreate(CourseBase):
    pass  # ✅ Hereda de CourseBase sin cambios

class Course(CourseBase):
    id: int  # Identificador único del curso

    class Config:
        orm_mode = True  #  Permite convertir instancias de SQLAlchemy a modelos Pydantic

# 🔹 Esquema de progreso de usuario en cursos
class UserCourseBase(BaseModel):
    course_id: int  # Identificador del curso en el que el usuario está inscrito

class UserCourse(UserCourseBase):
    id: int  # Identificador único del progreso del usuario en el curso
    completed: bool  #  Indica si el usuario ha completado el curso
    course: Course  # Relación con el curso al que está inscrito el usuario

    class Config:
        orm_mode = True  #  Permite la conversión automática de modelos ORM a Pydantic
