// Importación de módulos necesarios
import React, { useContext, useState } from "react";  // React y sus hooks para manejar estados y contexto
import axios from "axios";  // Librería para hacer peticiones HTTP
import { CartContext } from "../context/CartContext";  // Contexto del carrito de compras
import { AuthContext } from "../context/AuthContext";  // Contexto de autenticación de usuario
import "../styles/Cart.css";  // Importación de estilos CSS para el carrito

// Definición del componente Cart
const Cart = () => {
    const { cart, removeFromCart, clearCart } = useContext(CartContext);  // Obtención de estado y funciones del carrito desde su contexto
    const { user } = useContext(AuthContext);  // Obtención del usuario autenticado desde su contexto
    const [orderPlaced] = useState(false);  // Estado para verificar si se ha realizado un pedido

    // Cálculo del precio total sumando los precios de los productos según su cantidad
    const totalPrice = cart.reduce((total, item) => total + item.price * item.quantity, 0);

    // Función asincrónica para realizar un pedido
    const placeOrder = async () => {
        try {
            const user_id = localStorage.getItem("user_id");  // Obtiene el ID del usuario desde localStorage

            if (!user_id) {  // Verifica si el usuario está autenticado
                alert("No estás autenticado. Inicia sesión primero.");
                return;
            }

            // Creación del objeto con los datos del pedido
            const orderData = {
                user_id: Number(user_id),  // Convertir user_id a número
                total: cart.reduce((total, item) => total + item.price * item.quantity, 0),  // Calcula el total del pedido
                items: cart.map(item => ({  // Mapea los productos del carrito al formato del pedido
                    product_id: item.id,
                    title: item.title,
                    image: item.image,
                    quantity: item.quantity,
                    price: item.price
                }))
            };

            console.log("Enviando pedido:", orderData);  // Registro de depuración

            await axios.post("http://localhost:8000/orders", orderData);  // Envío de pedido al servidor

            alert("Pedido realizado correctamente.");  // Mensaje de confirmación
        } catch (error) {
            if (error.response) {
                console.error("Detalle del error:", error.response.data.detail);  // Muestra el detalle del error si la API responde con fallo
            } else {
                console.error("Error inesperado:", error.message);  // Manejo de errores inesperados
            }
        }
    };

    // Función para simular el pago del pedido
    const payOrder = () => {
        let orders = JSON.parse(localStorage.getItem("orders")) || [];  // Obtiene los pedidos almacenados
        orders.forEach(order => (order.status = "Pagado"));  // Cambia el estado de todos los pedidos a "Pagado"
        localStorage.setItem("orders", JSON.stringify(orders));  // Guarda los pedidos actualizados en localStorage
        clearCart();  // Vacía el carrito de compras
        alert("Pago realizado. ¡Gracias por tu compra!");  // Muestra mensaje de éxito
    };

    return (
        <div>
            <h1>Carrito de Compras</h1>
            {cart.length === 0 ? (  // Si el carrito está vacío, muestra un mensaje
                <p>Tu carrito está vacío</p>
            ) : (
                <>
                    {cart.map(item => (  // Itera sobre los productos del carrito para mostrarlos
                        <div key={item.id} className="cart-item">
                            <img src={item.image} alt={item.title} width="100" />  {/* Imagen del producto */}
                            <h3>{item.title}</h3>  {/* Nombre del producto */}
                            <p>Precio: {item.price} USD</p>  {/* Precio del producto */}
                            <p>Cantidad: {item.quantity}</p>  {/* Cantidad del producto */}
                            <button onClick={() => removeFromCart(item.id)}>Eliminar uno</button>  {/* Botón para eliminar una unidad */}
                        </div>
                    ))}

                    <div className="cart-summary">  {/* Resumen del carrito */}
                        <h2>Total: {totalPrice.toFixed(2)} USD</h2>  {/* Muestra el total de la compra */}
                        <button className="clear-btn" onClick={clearCart}>Vaciar Carrito</button>  {/* Botón para vaciar el carrito */}

                        {user ? (  // Si el usuario está autenticado, muestra opciones de orden y pago
                            orderPlaced ? (  // Si el pedido ya ha sido realizado, muestra el botón de pago
                                <button className="pay-btn" onClick={payOrder}>Pagar</button>
                            ) : (  // Si el pedido no ha sido realizado, muestra el botón para realizar el pedido
                                <button className="order-btn" onClick={placeOrder}>Ordenar</button>
                            )
                        ) : (
                            <p>Debes iniciar sesión para comprar</p>  // Mensaje cuando el usuario no está autenticado
                        )}
                    </div>
                </>
            )}
        </div>
    );
};

// Exportación del componente para su uso en otros archivos
export default Cart;
