// Importación de módulos necesarios
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";  // React Router para manejar la navegación
import Home from "./pages/Home";  // Página de inicio
import Cart from "./pages/Cart";  // Página del carrito de compras
import Orders from "./pages/Orders";  // Página de pedidos
import Login from "./pages/Login";  // Página de inicio de sesión
import Navbar from "./components/Navbar";  // Componente de barra de navegación
import GlobalStyle from "./GlobalStyle";  // Configuración global de estilos
import Register from "./pages/Register";  // Página de registro
import { CartProvider } from "./context/CartContext";  // Contexto global del carrito de compras
import { AuthProvider } from "./context/AuthContext";  // Contexto global de autenticación

// Definición del componente principal de la aplicación
function App() {
    return (
        <>
            {/* Proveedor de autenticación para manejar el estado del usuario */}
            <AuthProvider>
                {/* Proveedor del carrito de compras para manejar el estado de los productos en el carrito */}
                <CartProvider>
                    <GlobalStyle />  {/* Aplicación de estilos globales */}
                    <Router>  {/* Configuración del enrutador para manejar la navegación */}
                        <Navbar />  {/* Componente de barra de navegación */}
                        <Routes>
                            <Route path="/" element={<Home />} />  {/* Ruta de la página de inicio */}
                            <Route path="/cart" element={<Cart />} />  {/* Ruta de la página del carrito */}
                            <Route path="/orders" element={<Orders />} />  {/* Ruta de la página de pedidos */}
                            <Route path="/login" element={<Login />} />  {/* Ruta de la página de inicio de sesión */}
                            <Route path="/register" element={<Register />} />  {/* Ruta de la página de registro */}
                        </Routes>
                    </Router>
                </CartProvider>
            </AuthProvider>
        </>
    );
}

// Exportación del componente para su uso en otros archivos
export default App;