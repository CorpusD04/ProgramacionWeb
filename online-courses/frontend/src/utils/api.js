// Importa la biblioteca Axios para realizar solicitudes HTTP
import axios from "axios";

// Crea una instancia de Axios con configuración personalizada
const API = axios.create({
  baseURL: "http://localhost:8000", // Define la URL base de la API (cámbiala si es necesario)
  withCredentials: true, // Habilita el envío de cookies en solicitudes (si la API las requiere)
});

// Interceptor que agrega el token de autenticación a cada solicitud
API.interceptors.request.use((config) => {
  const token = getToken(); // Obtiene el token del almacenamiento local
  if (token) {
    config.headers.Authorization = `Bearer ${token}`; // Agrega el token a los encabezados de la petición
  }
  return config;
});

// Obtiene el ID del usuario desde el almacenamiento local (comentado pero útil para futuras mejoras)
// const userId = localStorage.getItem("user_id");

// Obtiene los datos del usuario almacenados en localStorage
const userData = localStorage.getItem("user");
const token = userData?.access_token; // Extrae el token de acceso si existe

// Función para obtener el token de autenticación almacenado en localStorage
const getToken = () => {
  const userData = localStorage.getItem("user");
  if (!userData) return null; // Si no hay datos, retorna null
  try {
    const parsed = JSON.parse(userData); // Intenta parsear los datos a formato JSON
    return parsed.access_token; // Devuelve el token de acceso si existe
  } catch (err) {
    return null; // Retorna null en caso de error de conversión
  }
};

// Función para obtener la lista de cursos desde la API
export const getCourses = () => API.get("/courses");

// Función para inscribir a un usuario en un curso específico
export const enrollCourse = (courseId) => {
  return API.post(`/courses/enroll/${courseId}`);
};

// Función para marcar un curso como completado
export const completeCourse = async (courseId) => {
  const token = localStorage.getItem("token"); // Obtiene el token almacenado

  if (!token) {
    console.error("No hay token para marcar como completado."); // Muestra un error en la consola
    return Promise.reject("Usuario no autenticado."); // Retorna una promesa rechazada
  }

  return API.post(`/courses/complete/${courseId}`, {}, {
    headers: { Authorization: `Bearer ${token}` } // Agrega el token en los encabezados de la petición
  });
};

// Función para obtener los cursos del perfil del usuario
export const getProfileCourses = () => {
  return axios.get("http://localhost:8000/profile/courses"); // Realiza una solicitud GET a la API
};

// Exporta la instancia de Axios para que pueda ser utilizada en otras partes del proyecto
export default API;
