// Importa módulos necesarios de React y React Router
import React, { useEffect, useState, useContext } from "react"; // Hooks para gestionar estado y efectos
import { useParams } from "react-router-dom"; // Hook para obtener parámetros de la URL
import { getCourses, enrollCourse, completeCourse } from "../utils/api"; // Funciones para interactuar con la API
import { AuthContext } from "../context/AuthContext";  // ✅ Contexto de autenticación para obtener el usuario actual
import "../App.css"; // Archivo CSS para estilos

// Define el componente funcional CourseDetail
function CourseDetail() {
  const { id } = useParams(); // Obtiene el ID del curso desde la URL
  const [course, setCourse] = useState(null); // Estado para almacenar los datos del curso
  const { user } = useContext(AuthContext); // Obtiene el usuario actual desde el contexto de autenticación

  // Hook useEffect para obtener los detalles del curso cuando cambia el ID
  useEffect(() => {
    getCourses().then((res) => { // Llama a la función de API para obtener la lista de cursos
      const found = res.data.find((c) => c.id === parseInt(id)); // Busca el curso correspondiente al ID
      setCourse(found); // Actualiza el estado con el curso encontrado
    });
  }, [id]); // Se ejecuta cuando cambia el ID del curso

  // Si el curso no está disponible, muestra un mensaje de carga
  if (!course) return <p>Cargando...</p>;

  // Si el usuario no está autenticado, muestra un mensaje y evita que se inscriba
  if (!user || !user.id) {
    console.error("Error: user_id no está definido correctamente.");
    return <p>Por favor, inicia sesión para inscribirte en el curso.</p>;
  }

  // Renderiza los detalles del curso y los botones de acción
  return (
    <div>
      <h2>{course.title}</h2> {/* Muestra el título del curso */}
      <p>{course.description}</p> {/* Muestra la descripción del curso */}
      <a href={course.url} target="_blank" rel="noreferrer">Ver curso</a> {/* Enlace para acceder al curso */}
      <br />
      <button onClick={() => enrollCourse(course.id)}>Inscribirse</button> {/* Botón para inscribirse */}
      <button onClick={() => completeCourse(course.id)}>Marcar como completado</button> {/* Botón para completar curso */}
    </div>
  );
}

// Exporta el componente para que pueda ser utilizado en otras partes de la aplicación
export default CourseDetail;
