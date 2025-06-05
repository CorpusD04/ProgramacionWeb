// Importa los módulos necesarios de React y React Router
import React, { useEffect, useState } from "react"; // Hooks para gestionar estado y efectos
import { getCourses, enrollCourse } from "../utils/api"; // Funciones para interactuar con la API de cursos
import { useNavigate } from "react-router-dom"; // Hook para manejar la navegación entre páginas
import "../App.css"; // Archivo de estilos CSS

// Define el componente funcional Courses
function Courses() {
  const [courses, setCourses] = useState([]); // Estado para almacenar la lista de cursos
  const navigate = useNavigate(); // Hook para navegar a diferentes rutas dentro de la aplicación

  // Hook useEffect para obtener la lista de cursos al cargar el componente
  useEffect(() => {
    getCourses()
      .then((res) => {
        console.log("Cursos recibidos:", res.data); // 👈 Verifica el contenido en la consola
        setCourses(res.data); // Almacena la lista de cursos en el estado
      })
      .catch((err) => {
        console.error("Error al cargar cursos", err); // Muestra errores en la consola si la carga falla
      });
  }, []);

  // Función para inscribir al usuario en un curso
  const handleEnroll = (courseId) => {
    enrollCourse(courseId)
      .then(() => alert("¡Inscripción exitosa!")) // Muestra una alerta si la inscripción fue exitosa
      .catch(() => alert("Ya estás inscrito o hubo un error")); // Muestra una alerta si ocurre un error
  };

  // Renderiza la interfaz de la lista de cursos
  return (
    <div style={{ padding: "20px" }}> {/* Contenedor principal con espaciado */}
      <h2>Cursos Disponibles</h2> {/* Título de la sección */}
      <div style={{ display: "flex", flexWrap: "wrap", gap: "20px" }}> {/* Diseño de cuadrícula flexible */}
        {courses.map((course) => ( // Mapea y muestra cada curso en la lista
          <div key={course.id} style={{ border: "1px solid #ccc", padding: "10px", width: "300px" }}> {/* Tarjeta de curso */}
            {course.image && (
              <img src={course.image} alt={course.title} style={{ width: "100%", height: "150px", objectFit: "cover" }} /> /* Muestra la imagen del curso si existe */
            )}
            <h3>{course.title}</h3> {/* Muestra el título del curso */}
            <p><strong>Categoría:</strong> {course.category}</p> {/* Muestra la categoría del curso */}
            <p>{course.description.slice(0, 100)}...</p> {/* Muestra un fragmento de la descripción */}
            <button onClick={() => navigate(`/courses/${course.id}`)}>Ver curso</button> {/* Botón para ver detalles del curso */}
            <button onClick={() => handleEnroll(course.id)}>Inscribirse</button> {/* Botón para inscribirse en el curso */}
          </div>
        ))}
      </div>
    </div>
  );
}

// Exporta el componente para que pueda ser utilizado en otras partes de la aplicación
export default Courses;
