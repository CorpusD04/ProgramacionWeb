// Importación del módulo necesario para definir estilos globales
import { createGlobalStyle } from "styled-components";  //  Herramienta de styled-components para crear estilos globales

// Creación de estilos globales utilizando createGlobalStyle
const GlobalStyle = createGlobalStyle`
   body {
     font-family: Arial, sans-serif;  /*  Define la fuente global */
     margin: 0;  /* 🔹 Elimina el margen predeterminado */
     padding: 0;  /* 🔹 Elimina el espacio interno predeterminado */
     background-color: #f5f5f5;  /*  Establece un fondo gris claro */
   }
`;

// Exportación del componente GlobalStyle para su uso en toda la aplicación
export default GlobalStyle;
