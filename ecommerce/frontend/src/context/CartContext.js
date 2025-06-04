// Importación de módulos necesarios
import { createContext, useState } from "react";  // Importa React y sus hooks

// Creación del contexto para el carrito de compras
export const CartContext = createContext();

export const CartProvider = ({ children }) => {
    // Estado para almacenar los productos en el carrito
    const [cart, setCart] = useState([]);

    // Función para agregar productos al carrito agrupados por ID
    const addToCart = (product) => {
        setCart(prevCart => {
            const existingProduct = prevCart.find(item => item.id === product.id);  // Verifica si el producto ya está en el carrito
            if (existingProduct) {
                return prevCart.map(item =>
                    item.id === product.id ? { ...item, quantity: item.quantity + 1 } : item
                );  // Si el producto ya existe, aumenta su cantidad en 1
            } else {
                return [...prevCart, { ...product, quantity: 1 }];  // Si el producto no está, lo agrega con cantidad 1
            }
        });
    };

    // Función para eliminar solo una unidad del producto del carrito
    const removeFromCart = (productId) => {
        setCart(prevCart => {
            const updatedCart = prevCart.map(item =>
                item.id === productId ? { ...item, quantity: item.quantity - 1 } : item
            ).filter(item => item.quantity > 0);  // 🔹 Filtra productos con cantidad mayor a 0
            return updatedCart;
        });
    };

    // Función para vaciar completamente el carrito
    const clearCart = () => setCart([]);  // 🗑️ Elimina todos los productos del carrito

    // Retorno del proveedor de contexto con las funciones de manejo del carrito
    return (
        <CartContext.Provider value={{ cart, addToCart, removeFromCart, clearCart }}>
            {children}  {/* Renderiza los componentes hijos dentro del contexto */}
        </CartContext.Provider>
    );
};