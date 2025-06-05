import { useEffect, useState } from "react";
import { createContext } from "react";  // ✅ Importar `createContext`

export const AuthContext = createContext();  // ✅ Crear el contexto sin errores

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);

 useEffect(() => {
  const storedUser = localStorage.getItem("user");
  try {
    const parsedUser = JSON.parse(storedUser);
    if (parsedUser && parsedUser.id) {
      setUser(parsedUser);
    }
  } catch (e) {
    console.error("Error al parsear el usuario:", e);
  }
}, []);


  return (
    <AuthContext.Provider value={{ user, setUser }}>
      {children}
    </AuthContext.Provider>
  );
};
