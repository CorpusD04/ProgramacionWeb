# Importa la configuración de la base de datos y el modelo de cursos
from app.database import SessionLocal  # Manejo de sesiones con la base de datos
from app.models import Course  # Modelo de curso definido en SQLAlchemy

# 🔹 Lista de cursos a insertar en la base de datos
courses = [
    {
        "title": "JavaScript Full Course – freeCodeCamp",  # Título del curso
        "description": "Curso completo de JavaScript desde cero.",  # Descripción del curso
        "category": "programación",  # Categoría del curso
        "url": "https://www.youtube.com/watch?v=jS4aFq5-91M",  # URL del curso
        "provider": "YouTube",  # Plataforma que ofrece el curso
        "image": "https://img.youtube.com/vi/jS4aFq5-91M/hqdefault.jpg"  # Imagen asociada al curso
    },
    {
        "title": "Python para principiantes",  # Título del curso
        "description": "Aprende Python desde cero en español.",  # Descripción del curso
        "category": "programación",  # Categoría del curso
        "url": "https://www.youtube.com/watch?v=Kp4Mvapo5kc",  # URL del curso
        "provider": "YouTube",  # Plataforma que ofrece el curso
        "image": "https://img.youtube.com/vi/Kp4Mvapo5kc/hqdefault.jpg"  # Imagen asociada al curso
    },
    # ✅ Puedes agregar más cursos aquí...
]

# 🔹 Inicia una sesión en la base de datos
db = SessionLocal()

# Itera sobre la lista de cursos y los inserta en la base de datos
for course in courses:
    db_course = Course(**course)  # Crea una instancia del modelo `Course` con los datos del curso
    db.add(db_course)  # Agrega el curso a la sesión

# Guarda los cambios en la base de datos y cierra la sesión
db.commit()  # ✅ Confirma las inserciones en la base de datos
db.close()  # ✅ Cierra la sesión para liberar recursos
