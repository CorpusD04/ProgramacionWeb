// Importa la biblioteca React para definir un componente funcional
import React from "react";
// Importa el componente Link de react-router-dom para manejar la navegación interna
import { Link } from "react-router-dom";

// Define el componente Navbar como una función de React
const Navbar = () => {
    return (
        <nav> {/* Elemento HTML para la barra de navegación */}
            <h1>Online Courses</h1> {/* Título de la barra de navegación */}
            <ul> {/* Lista de elementos de navegación */}
                <li><Link to="/">Inicio</Link></li> {/* Enlace a la página de inicio */}
                <li><Link to="/courses">Cursos</Link></li> {/* Enlace a la página de cursos */}
                <li><Link to="/profile">Perfil</Link></li> {/* Enlace al perfil del usuario */}
                <li><Link to="/login">Iniciar sesión</Link></li>  {/* Enlace a la página de inicio de sesión */}
            </ul>
        </nav>
    );
};

// Exporta el componente para que pueda ser utilizado en otros archivos
export default Navbar;
