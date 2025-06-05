// Importa los módulos necesarios de React Router para manejar la navegación
import { Routes, Route } from "react-router-dom"; 

// Importa los componentes utilizados en la aplicación
import Navbar from "./components/Navbar"; // Barra de navegación
import Home from "./pages/Home"; // Página principal
import Courses from "./pages/Courses"; // Página de cursos disponibles
import CourseDetail from "./pages/CourseDetail"; // Página de detalles de un curso
import Profile from "./pages/Profile"; // Página de perfil del usuario
import Footer from "./components/Footer"; // Pie de página
import Register from "./pages/Register"; // Página de registro de usuario
import Login from "./pages/Login"; // Página de inicio de sesión

// Importa el proveedor de autenticación para manejar el estado de usuario
import { AuthProvider } from "./context/AuthContext"; 

// Define el componente principal de la aplicación
const App = () => {
    return (
        <div> {/* Contenedor principal de la aplicación */}
            <AuthProvider> {/* Envuelve toda la aplicación con el contexto de autenticación */}
                <Navbar /> {/* Barra de navegación superior */}
                <Routes> {/* Contenedor de rutas para manejar la navegación */}
                    <Route path="/" element={<Home />} /> {/* Ruta para la página de inicio */}
                    <Route path="/courses" element={<Courses />} /> {/* Ruta para la lista de cursos */}
                    <Route path="/courses/:id" element={<CourseDetail />} /> {/* Ruta para los detalles de un curso en específico */}
                    <Route path="/profile" element={<Profile />} /> {/* Ruta para la página de perfil del usuario */}
                    <Route path="/register" element={<Register />} /> {/* Ruta para la página de registro */}
                    <Route path="/login" element={<Login />} /> {/* Ruta para la página de inicio de sesión */}
                </Routes>
                <Footer /> {/* Pie de página */}
            </AuthProvider>
        </div>
    );
};

// Exporta el componente para que pueda ser utilizado en otras partes de la aplicación
export default App;
