// Importa módulos esenciales de React para manejar estado, efectos y contexto
import React, { useEffect, useState, useContext } from "react"; 
import { getProfileCourses } from "../utils/api"; // API para obtener los cursos del perfil
import "../App.css"; // Importa el archivo de estilos CSS
import { AuthContext } from "../context/AuthContext"; // Contexto de autenticación para manejar el usuario

// Define el componente funcional Profile
function Profile() {
  const { user } = useContext(AuthContext); // Obtiene el usuario desde el contexto de autenticación
  const [inProgress, setInProgress] = useState([]); // Estado para almacenar los cursos en progreso
  const [completed, setCompleted] = useState([]); // Estado para almacenar los cursos completados

  // Hook useEffect para obtener los cursos del usuario cuando cambia el estado de autenticación
  useEffect(() => {
    if (user && user.id) { // ✅ Asegurar que `user` y `user.id` existen antes de hacer la solicitud
      getProfileCourses()
        .then((res) => {
          const cursos = res.data; // Obtiene los datos de los cursos desde la API
          setInProgress(cursos.filter((c) => !c.completed)); // Filtra los cursos en progreso
          setCompleted(cursos.filter((c) => c.completed)); // Filtra los cursos completados
        })
        .catch((err) => console.error("Error al obtener cursos:", err)); // Manejo de errores si falla la solicitud      
    }
  }, [user]);
// Retorno de la interfaz de usuario
return (
    <div> {/* Contenedor principal */}
      <h2>Perfil</h2> {/* Título de la página de perfil */}

      <h3>Cursos en curso</h3> {/* Subtítulo de cursos en progreso */}
      {inProgress.length === 0 ? ( 
        <p>No hay cursos en curso.</p> /* Mensaje cuando no hay cursos en progreso */
      ) : (
        inProgress.map((c) => <p key={c.id}>{c.title}</p>) /* Lista de cursos en progreso */
      )}

      <h3>Cursos completados</h3> {/* Subtítulo de cursos completados */}
      {completed.length === 0 ? ( 
        <p>No has completado ningún curso.</p> /* Mensaje cuando no hay cursos completados */
      ) : (
        completed.map((c) => <p key={c.id}>{c.title}</p>) /* Lista de cursos completados */
      )}
    </div>
);
}

// Exportación del componente para que pueda usarse en otras partes de la aplicación
export default Profile;
