// Importación de módulos necesarios
import React, { useState, useEffect, useContext } from "react";  // React y sus hooks para manejar estados, efectos y contexto
import { getProducts } from "../services/api";  // Función para obtener productos desde la API
import { CartContext } from "../context/CartContext";  // Contexto global del carrito de compras
import axios from "axios";  // Librería para hacer solicitudes HTTP
import "../styles/Home.css";  // Importación de estilos CSS para la página principal

// Definición del componente Home
const Home = () => {
    // Estado para almacenar los productos obtenidos desde la API
    const [products, setProducts] = useState([]);

    // Obtención de la función para agregar productos al carrito desde el contexto global
    const { addToCart } = useContext(CartContext);

    // Hook useEffect para cargar los productos al montar el componente
    useEffect(() => {
        axios.get("http://localhost:8000/products")  // Solicitud HTTP a la API local para obtener productos
            .then(response => setProducts(response.data))  // Almacena los productos obtenidos en el estado
            .catch(error => console.error("Error al obtener productos:", error));  // Manejo de errores en la solicitud

        getProducts().then(setProducts);  // Alternativa para obtener productos usando la función importada
    }, []);

    return (
        <div className="product-container">  {/* Contenedor principal de los productos */}
            {Array.isArray(products) ? (  // Verifica si products es un array antes de mapearlo
                products.map(product => (  // Itera sobre los productos para mostrarlos en tarjetas
                    <div key={product.id} className="product-card">
                        <img src={product.image} alt={product.title} className="product-image" />  {/* Imagen del producto */}
                        <h3>{product.name}</h3>  {/* Nombre del producto */}
                        <p>{product.price} USD</p>  {/* Precio del producto */}
                        <button onClick={() => addToCart(product)}>Añadir al carrito</button>  {/* Botón para agregar al carrito */}
                    </div>
                ))
            ) : (
                <p>Cargando productos...</p>  // Mensaje mostrado mientras se cargan los productos
            )}
        </div>
    );
};

// Exportación del componente Home para su uso en otros archivos
export default Home;