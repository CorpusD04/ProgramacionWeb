# Importa los módulos necesarios
import json  # Manejo de archivos JSON
from sqlalchemy.orm import Session  # Manejo de sesiones en SQLAlchemy
from app.database import SessionLocal  # Configuración de la sesión de la base de datos
from app.models import Course  # Modelo de cursos en la base de datos

# 🔹 Función para insertar cursos desde un archivo JSON
def insert_courses_from_json(json_file: str):
    db: Session = SessionLocal()  # Inicia una sesión de base de datos
    try:
        with open(json_file, 'r', encoding='utf-8') as file:
            courses_data = json.load(file)  # Carga los datos del archivo JSON

        for course in courses_data:
            # Verifica si el curso ya existe en la base de datos
            exists = db.query(Course).filter_by(title=course["title"], url=course["url"]).first()
            if not exists:
                # Crea una nueva entrada en la base de datos
                new_course = Course(
                    title=course["title"],
                    description=course["description"],
                    category=course["category"],
                    provider=course["provider"],
                    url=course["url"]
                )
                db.add(new_course)  # Agrega el curso a la sesión
                print(f"Curso insertado: {course['title']}")  # Mensaje de éxito
            else:
                print(f"Ya existe: {course['title']}")  # Mensaje si el curso ya está registrado

        db.commit()  # Confirma los cambios en la base de datos
    except Exception as e:
        print(f"Error: {e}")  # Captura y muestra errores durante el proceso
    finally:
        db.close()  # Cierra la sesión de la base de datos

# 🔹 Ejecutar la función si el script se ejecuta directamente
if __name__ == "__main__":
    insert_courses_from_json("public_courses.json")  # Llama a la función con el archivo JSON
