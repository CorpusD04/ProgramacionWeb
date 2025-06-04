// Importación de módulos necesarios
import { useNavigate } from "react-router-dom";  // Hook para manejar la navegación entre rutas
import { FaShoppingCart } from "react-icons/fa";  // Icono de carrito de compras de FontAwesome
import "../styles/Navbar.css";  // Importación de estilos CSS para la barra de navegación
import { useContext } from "react";  // Hook para acceder al contexto de React
import { CartContext } from "../context/CartContext";  // Contexto global del carrito de compras

// Definición del componente Navbar
const Navbar = () => {
    const navigate = useNavigate();  // Hook para manejar la navegación
    const { cart } = useContext(CartContext);  // Obtención del carrito desde el contexto global

    // Cálculo del número total de productos en el carrito
    const totalItems = cart.reduce((total, item) => total + item.quantity, 0);

    return (
        <nav className="navbar">  {/* Elemento de barra de navegación */}
            <h1 className="title">eCommerce</h1>  {/* Título de la aplicación */}

            <div className="nav-buttons">  {/* Contenedor de los botones de navegación */}
                <button onClick={() => navigate("/")}>Inicio</button>  {/* Botón para ir a la página principal */}
                <button onClick={() => navigate("/orders")}>Pedidos</button>  {/* Botón para ir a la página de pedidos */}
                <button onClick={() => navigate("/login")}>Login</button>  {/* Botón para ir a la página de login */}
                <button onClick={() => navigate("/cart")}>  {/* Botón para ir al carrito de compras */}
                    <FaShoppingCart className="cart-icon" /> 🛒  {/* Icono de carrito de compras */}
                    <span className="cart-count">{totalItems}</span> {/* 🔹 Muestra el total de productos en el carrito */}
                </button>
            </div>
        </nav>
    );
};

// Exportación del componente Navbar para su uso en otros archivos
export default Navbar;