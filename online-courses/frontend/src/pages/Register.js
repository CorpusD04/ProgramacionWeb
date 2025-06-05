// Importa los módulos necesarios de React y Axios para manejar el formulario y las solicitudes HTTP
import React, { useState } from "react"; // Hook para gestionar el estado del formulario
import axios from "axios"; // Librería para hacer peticiones HTTP
import { useNavigate } from "react-router-dom"; // Hook para redirigir a otra página después del registro
import "../App.css"; // Archivo de estilos CSS

// Define el componente funcional Register
const Register = () => {
    const [formData, setFormData] = useState({ name: "", email: "", password: "" }); // Estado para almacenar los datos del formulario
    const navigate = useNavigate(); // Hook para manejar la navegación dentro de la aplicación

    // Función para actualizar el estado del formulario cuando el usuario escribe en los campos
    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    // Función para manejar el envío del formulario de registro
    const handleSubmit = async (e) => {
        e.preventDefault(); // Previene la recarga de la página al enviar el formulario
        try {
            // Realiza una solicitud POST al servidor con los datos del usuario
            await axios.post("http://localhost:8000/auth/register", formData);
            alert("Registro exitoso. Ahora puedes iniciar sesión."); // Muestra una alerta de éxito
            navigate("/login"); // Redirige al usuario a la página de inicio de sesión
        } catch (error) {
            alert("Error al registrarse: " + (error.response?.data?.detail || "Inténtalo de nuevo.")); // Muestra un mensaje de error si el registro falla
        }
    };

    // Renderiza el formulario de registro
    return (
        <div>
            <h1>Registro de usuario</h1> {/* Encabezado principal */}
            <form onSubmit={handleSubmit}> {/* Formulario que ejecuta handleSubmit al enviarse */}
                <input 
                    type="text" name="name" placeholder="Nombre completo" 
                    onChange={handleChange} required 
                /> {/* Campo para ingresar el nombre del usuario */}

                <input 
                    type="email" name="email" placeholder="Correo electrónico" 
                    onChange={handleChange} required 
                /> {/* Campo para ingresar el correo electrónico */}

                <input 
                    type="password" name="password" placeholder="Contraseña" 
                    onChange={handleChange} required 
                /> {/* Campo para ingresar la contraseña */}

                <button type="submit">Registrarse</button> {/* Botón para enviar el formulario */}
            </form>
        </div>
    );
};

// Exporta el componente para que pueda ser utilizado en otras partes de la aplicación
export default Register;
