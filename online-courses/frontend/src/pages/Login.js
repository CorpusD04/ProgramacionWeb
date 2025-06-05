// Importa los módulos necesarios de React y Axios para manejar el formulario y las solicitudes HTTP
import React, { useState } from "react"; // Hook para gestionar el estado del formulario
import axios from "axios"; // Librería para hacer peticiones HTTP
import { useNavigate } from "react-router-dom"; // Hook para redirigir a otra página
import "../App.css"; // Archivo CSS para estilos

// Define el componente funcional Login
const Login = () => {
    const [formData, setFormData] = useState({ email: "", password: "" }); // Estado para almacenar los datos ingresados
    const navigate = useNavigate(); // Hook para manejar la navegación

    // Función para actualizar el estado del formulario cuando el usuario escribe en los campos
    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    // Función para manejar el envío del formulario de inicio de sesión
    const handleSubmit = async (e) => {
        e.preventDefault(); // Previene la recarga de la página

        try {
            // Realiza una solicitud POST al servidor con los datos de inicio de sesión
            const response = await axios.post("http://localhost:8000/auth/login", {
                email: formData.email, 
                password: formData.password
            }, {
                headers: { "Content-Type": "application/json" },
            });

            // Guarda los datos del usuario en localStorage (puede incluir ID y token)
            localStorage.setItem("user", JSON.stringify(response.data)); // ✅ Guarda el ID del usuario
            // localStorage.setItem("token", response.data.access_token); // ✅ Guarda el token de acceso

            // Redirige al usuario a su perfil después de un inicio de sesión exitoso
            navigate("/profile");
        } catch (error) {
            alert("Error al iniciar sesión: " + error.response?.data?.detail || "Intenta nuevamente");
        }
    };

    // Renderiza el formulario de inicio de sesión
    return (
        <div>
            <h1>Iniciar sesión</h1> {/* Encabezado de la página */}
            <form onSubmit={handleSubmit}> {/* Formulario que activa la función handleSubmit */}
                <input 
                    type="email" name="email" placeholder="Correo electrónico" 
                    onChange={handleChange} required 
                /> {/* Campo para ingresar el correo electrónico */}

                <input 
                    type="password" name="password" placeholder="Contraseña" 
                    onChange={handleChange} required 
                /> {/* Campo para ingresar la contraseña */}

                <button type="submit">Ingresar</button> {/* Botón para enviar el formulario */}

                <p>¿No tienes cuenta? <a href="/register">Regístrate aquí</a></p> {/* Enlace para el registro */}
            </form>
        </div>
    );
};

// Exporta el componente para que pueda ser utilizado en otras partes de la aplicación
export default Login;
