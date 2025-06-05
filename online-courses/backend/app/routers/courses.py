# Importa los módulos necesarios de FastAPI y SQLAlchemy
from fastapi import APIRouter, Depends, HTTPException, Body  # Manejo de rutas y dependencias en FastAPI
from sqlalchemy.orm import Session  # Manejo de sesiones para interactuar con la base de datos
from typing import List  # Tipo de datos para listas
from app.database import get_db  # Función para obtener la sesión de la base de datos
from app import models, schemas  # Importa los modelos y esquemas de datos
from app.routers.users import get_current_user  # Función para obtener el usuario autenticado
from app.models import UserCourse  # Modelo de relación entre usuario y cursos
from pydantic import BaseModel  # Validación de datos con Pydantic

# Define un enrutador con el prefijo "/courses" y etiqueta "Courses"
router = APIRouter(prefix="/courses", tags=["Courses"])

# Ruta para listar los cursos disponibles, opcionalmente filtrados por categoría
@router.get("/", response_model=List[schemas.Course])
def list_courses(category: str = None, db: Session = Depends(get_db)):
    query = db.query(models.Course)  # Consulta la tabla de cursos
    if category:  # Si se proporciona una categoría, filtra los resultados
        query = query.filter(models.Course.category == category)
    return query.all()  # Retorna la lista de cursos

# Ruta para inscribir a un usuario en un curso
@router.post("/enroll/{course_id}")
def enroll_course(course_id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    user_id = user.id  # Obtiene el ID del usuario autenticado

    if not user_id:  # Verifica si el usuario está autenticado
        raise HTTPException(status_code=400, detail="Se requiere user_id")

    # Verifica si el usuario ya está inscrito en el curso
    exists = db.query(UserCourse).filter_by(user_id=user_id, course_id=course_id).first()
    if exists:
        raise HTTPException(status_code=400, detail="Ya estás inscrito en este curso.")

    # Crea una nueva entrada en la tabla de cursos del usuario
    user_course = UserCourse(user_id=user_id, course_id=course_id)
    db.add(user_course)  # Agrega la inscripción
    db.commit()  # Confirma los cambios en la base de datos

    return {"message": "Inscrito exitosamente"}  # Retorna un mensaje de éxito

# Ruta para marcar un curso como completado
@router.post("/complete/{course_id}")
def complete_course(course_id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    # Busca la inscripción del usuario en el curso
    record = db.query(models.UserCourse).filter_by(user_id=user.id, course_id=course_id).first()
    if not record:  # Si el usuario no está inscrito, retorna un error
        raise HTTPException(status_code=404, detail="No estás inscrito en este curso.")
    record.completed = True  # Marca el curso como completado
    db.commit()  # Guarda los cambios en la base de datos

    return {"message": "Curso marcado como completado"}  # Retorna un mensaje de éxito
