// Importa la biblioteca React para definir un componente funcional
import React from "react";
// Importa los estilos desde el archivo CSS
import "../App.css";

// Define el componente Home como una función de React
const Home = () => {
    return (
        <div> {/* Contenedor principal */}
            <h1>Bienvenido a la plataforma de cursos</h1> {/* Encabezado principal */}
            <p>Explora cursos de diferentes proveedores y mejora tus habilidades.</p> {/* Mensaje informativo */}
        </div>
    );
};

// Exporta el componente para que pueda ser utilizado en otras partes de la aplicación
export default Home;
