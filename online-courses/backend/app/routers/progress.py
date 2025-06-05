# Importa módulos necesarios de FastAPI y SQLAlchemy
from fastapi import APIRouter, Depends  # FastAPI para definir rutas y gestionar dependencias
from sqlalchemy.orm import Session  # SQLAlchemy para interactuar con la base de datos
from app import models, schemas  # Importa los modelos y esquemas definidos en la aplicación
from app.database import get_db  # Función para obtener la sesión de la base de datos
from app.routers.users import get_current_user  # Función para obtener el usuario autenticado
from app.schemas import CourseOut  # Esquema para representar los cursos del usuario
from typing import List  # Tipo de datos List para respuestas con múltiples elementos
from app.models import User  # Modelo de usuario

# Define el enrutador con el prefijo "/profile" y la etiqueta "Perfil"
router = APIRouter(prefix="/profile", tags=["Perfil"])

# Ruta para obtener los cursos inscritos y completados por el usuario
@router.get("/profile/courses", response_model=List[CourseOut])
def get_user_courses(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Consulta todos los cursos en los que el usuario está inscrito usando su ID
    all_courses = db.query(models.UserCourse).filter_by(user_id=current_user.id).all()  # ✅ Usa `current_user.id`
    
    # Filtra los cursos en progreso (no completados)
    ongoing = [c for c in all_courses if not c.completed]
    
    # Filtra los cursos completados
    completed = [c for c in all_courses if c.completed]

    # Retorna un diccionario con cursos en progreso y completados
    return {
        "enrolled": ongoing,  # Lista de cursos en progreso
        "completed": completed  # Lista de cursos completados
    }
