// Importación de módulos necesarios
import React, { useState, useEffect } from "react";  // React y sus hooks para manejar estado y efectos
import axios from "axios";  // Librería para hacer solicitudes HTTP
import "../styles/Orders.css";  // Importación de estilos CSS para la página de pedidos

// Definición del componente Orders
const Orders = () => {
    // Estado para almacenar los pedidos obtenidos desde la API
    const [orders, setOrders] = useState([]);

    // Hook useEffect para cargar los pedidos cuando el componente se monta
    useEffect(() => {
        fetchOrders();  // Llama a la función que obtiene los pedidos
    }, []);

    // Función para obtener los pedidos desde la API
    const fetchOrders = () => {
        axios.get("http://localhost:8000/orders")  // Solicitud HTTP para obtener pedidos
            .then(response => {
                console.log("Pedidos recibidos:", response.data);  // Depuración en consola
                setOrders(response.data);  // Actualiza el estado con los pedidos obtenidos
            })
            .catch(error => console.error("Error al obtener pedidos:", error));  // Manejo de errores en la solicitud
    };

    // Función para pagar un producto del pedido
    const handlePay = async (itemId) => {
        try {
            await axios.post(`http://localhost:8000/orders/pay/${itemId}`);  // Solicitud de pago a la API
            fetchOrders();  // Refresca la lista de pedidos después del pago
        } catch (error) {
            console.error("Error al pagar producto:", error);  // Manejo de errores en la solicitud de pago
        }
    };

    // Función para eliminar un producto específico del pedido
    const handleDelete = async (itemId) => {
        try {
            await axios.delete(`http://localhost:8000/orders/item/${itemId}`);  // Solicitud de eliminación a la API
            fetchOrders();  // Refresca la lista de pedidos después de eliminar el producto
        } catch (error) {
            console.error("Error al eliminar producto:", error);  // Manejo de errores en la solicitud de eliminación
        }
    };

    return (
        <div>
            <h1>Mis Pedidos</h1>
            {orders && orders.length > 0 ? (  // Verifica si hay pedidos antes de mostrarlos
                <table className="orders-table">  {/* Tabla para visualizar los pedidos */}
                    <thead>
                        <tr>
                            <th>Imagen</th>
                            <th>Producto</th>
                            <th>Cantidad</th>
                            <th>Precio Total</th>
                            <th>Status</th>
                            <th>Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
                        {orders.map(order =>  // Itera sobre los pedidos obtenidos
                            order.order_items?.map(item => (  // Itera sobre los productos dentro de cada pedido
                                <tr key={item.id}>
                                    <td><img src={item.image} alt={item.title} width="50" /></td>  {/* Imagen del producto */}
                                    <td>{item.title}</td>  {/* Nombre del producto */}
                                    <td>{item.quantity}</td>  {/* Cantidad del producto */}
                                    <td>{(item.price * item.quantity).toFixed(2)} USD</td>  {/* Precio total */}
                                    <td>{item.status}</td>  {/* Estado del pedido */}
                                    <td>  {/* Botones de acción */}
                                        {item.status !== "Pagado" && (  // Muestra el botón de pago si el producto no ha sido pagado
                                            <button onClick={() => handlePay(item.id)}>Pagar</button>
                                        )}
                                        <button onClick={() => handleDelete(item.id)}>Eliminar</button>  {/* Botón para eliminar el producto */}
                                    </td>
                                </tr>
                            ))
                        )}
                    </tbody>
                </table>
            ) : (
                <p>No tienes pedidos.</p>  
            )}   {/* Mensaje si no hay pedidos disponibles */}
        </div>
    );
};

// Exportación del componente para su uso en otros archivos
export default Orders;