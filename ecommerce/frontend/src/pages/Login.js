// Importación de módulos necesarios
import React, { useState, useContext } from "react";  // React y sus hooks para manejar estados y contexto
import { useNavigate } from "react-router-dom";  // Hook para navegar entre rutas
import axios from "axios";  // Librería para realizar solicitudes HTTP
import { AuthContext } from "../context/AuthContext";  // Contexto de autenticación de usuario
import "../styles/AuthStyles.css";  // Importación de estilos CSS para la página de autenticación

// Definición del componente Login
const Login = () => {
    // Estado para almacenar los datos del formulario de inicio de sesión
    const [formData, setFormData] = useState({ email: "", password: "" });

    // Obtención del usuario autenticado y funciones de manejo de sesión desde el contexto global
    const { user, login, logout } = useContext(AuthContext);

    // Hook para manejar la navegación entre páginas
    const navigate = useNavigate();

    // Función para manejar cambios en los campos del formulario
    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    // Función para manejar el envío del formulario y autenticar al usuario
    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post("http://localhost:8000/auth/login", {
                email: formData.email,
                password: formData.password
            });

            localStorage.setItem("user_id", response.data.user_id);  // ✅ Guarda el ID del usuario en localStorage
            alert("Inicio de sesión exitoso");  // Mensaje de confirmación
            login(response.data);  // Actualiza el estado de autenticación en el contexto
            navigate("/");  // Redirige a la página principal
        } catch (error) {
            console.error("Error en el inicio de sesión:", error.response?.data);  // Manejo de errores en la autenticación
            alert("Error al iniciar sesión");  // Mensaje de error
        }
    };

    return (
        <div className="auth-container">  {/* Contenedor principal */}
            <div className="auth-box">  {/* Caja de autenticación */}
                {user ? (  // Si el usuario ya ha iniciado sesión, muestra su información
                    <>
                        <h2>Sesión Iniciada</h2>
                        <p>Bienvenido, {user.username}</p>
                        <button className="logout-btn" onClick={logout}>Cerrar Sesión</button>  {/* Botón para cerrar sesión */}
                    </>
                ) : (  // Si el usuario no ha iniciado sesión, muestra el formulario de autenticación
                    <>
                        <h2>Iniciar Sesión</h2>
                        <form onSubmit={handleSubmit}>
                            <input type="email" name="email" placeholder="Correo electrónico" onChange={handleChange} required />  {/* Campo de email */}
                            <input type="password" name="password" placeholder="Contraseña" onChange={handleChange} required />  {/* Campo de contraseña */}
                            <button type="submit">Iniciar Sesión</button>  {/* Botón para enviar el formulario */}
                        </form>
                        <p>No tienes una cuenta?</p>
                        <button onClick={() => navigate("/register")}>Regístrate aquí</button>  {/* Botón para navegar al registro */}
                    </>
                )}
            </div>
        </div>
    );
};

// Exportación del componente para su uso en otros archivos
export default Login;