// Importación de la librería Axios para realizar solicitudes HTTP
import axios from "axios";

// Función asincrónica para obtener la lista de productos desde la API
export const getProducts = async () => {
    try {
        const response = await axios.get("http://localhost:8000/products");  // ✅ Realiza una solicitud GET a la API
        console.log("Productos recibidos:", response.data);  // 📌 Registra los datos obtenidos en consola para depuración
        return response.data;  // Retorna la lista de productos obtenidos
    } catch (error) {
        console.error("Error al obtener productos:", error);  // 🚨 Manejo de errores en la solicitud
        return [];  // 🔹 Retorna un array vacío para evitar errores al utilizar .map() en la interfaz
    }
};
