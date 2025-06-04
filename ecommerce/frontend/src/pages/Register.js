// Importación de módulos necesarios
import React, { useState } from "react";  // React y su hook para manejar estados
import axios from "axios";  // Librería para realizar solicitudes HTTP
import "../styles/AuthStyles.css";  // Importación de estilos CSS para la página de registro

// Definición del componente Register
const Register = () => {
    // Estado para almacenar los datos del formulario de registro
    const [formData, setFormData] = useState({ username: "", email: "", password: "", region: "", address: "" });

    // Función para manejar cambios en los campos del formulario
    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });  // Actualiza el estado con los nuevos valores
    };

    // Función para manejar el envío del formulario y registrar al usuario
    const handleSubmit = async (e) => {
        e.preventDefault();  // Evita la recarga de la página
        try {
            await axios.post("http://localhost:8000/auth/register", {  // Solicitud HTTP para registrar un usuario
                username: formData.username,  // Nombre de usuario
                email: formData.email,  // Correo electrónico
                password: formData.password,  // Contraseña
                region: formData.region,  // Región
                address: formData.address  // Dirección
            });
            alert("Registro exitoso");  // Mensaje de confirmación
        } catch (error) {
            console.error("Error en el registro:", error.response.data);  // Manejo de errores en la solicitud de registro
            alert("Error en el registro");  // Mensaje de error
        }
    };

    return (
        <div className="auth-container">  {/* Contenedor principal */}
            <div className="auth-box">  {/* Caja de registro */}
                <h2>Registro</h2>
                <form onSubmit={handleSubmit}>  {/* Formulario de registro */}
                    <input type="text" name="username" placeholder="Nombre de usuario" onChange={handleChange} required />  {/* Campo de nombre de usuario */}
                    <input type="email" name="email" placeholder="Correo electrónico" onChange={handleChange} required />  {/* Campo de correo electrónico */}
                    <input type="password" name="password" placeholder="Contraseña" onChange={handleChange} required />  {/* Campo de contraseña */}
                    <input type="text" name="region" placeholder="Región" onChange={handleChange} required />  {/* Campo de región */}
                    <input type="text" name="address" placeholder="Dirección" onChange={handleChange} required />  {/* Campo de dirección */}
                    <button type="submit">Registrarse</button>  {/* Botón para enviar el formulario */}
                </form>
            </div>
        </div>
    );
};

// Exportación del componente para su uso en otros archivos
export default Register;