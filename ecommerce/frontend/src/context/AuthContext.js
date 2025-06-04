// Importación de módulos necesarios
import { createContext, useState, useEffect } from "react";  // Importa React y sus hooks

// Creación del contexto de autenticación
export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    // Estado para almacenar el usuario actual
    const [user, setUser] = useState(() => {
        return JSON.parse(localStorage.getItem("user")) || null;  // Obtiene el usuario desde localStorage si existe
    });

    // Función para manejar el inicio de sesión y guardar la información del usuario en localStorage
    const login = (userData) => {
        setUser(userData);
        localStorage.setItem("user", JSON.stringify(userData));  // ✅ Guarda el usuario en localStorage
    };

    // Función para manejar el cierre de sesión y eliminar la información del usuario de localStorage
    const logout = () => {
        setUser(null);
        localStorage.removeItem("user");  // 🗑️ Elimina la información del usuario al cerrar sesión
    };

    // Efecto para verificar si hay un usuario almacenado en localStorage cuando se monta el componente
    useEffect(() => {
        const storedUser = localStorage.getItem("user");
        if (storedUser) {
            setUser(JSON.parse(storedUser));  // ✅ Si hay un usuario guardado, lo establece en el estado
        }
    }, []);

    // Retorno del proveedor de contexto con las funciones de autenticación
    return (
        <AuthContext.Provider value={{ user, login, logout }}>
            {children}  {/* Renderiza los componentes hijos dentro del contexto */}
        </AuthContext.Provider>
    );
};