# Importa el módulo pymysql, que permite trabajar con bases de datos MySQL desde Python
import pymysql

# ------------------------------------------
# Definición de parámetros de conexión
# ------------------------------------------

# Dirección del servidor de base de datos
hostname = 'localhost'

# Puerto del servidor MySQL. Por defecto es 3306, pero aquí se usa 3307
port = 3307

# Nombre de usuario para conectarse al servidor de MySQL
user = 'root'

# Contraseña del usuario root. 
password = 'fairy15'  

# ------------------------------------------
# Crear conexión a MySQL sin seleccionar base de datos
# ------------------------------------------

# Establece una conexión a MySQL usando los datos anteriores, pero sin especificar una base de datos aún
db = pymysql.connections.Connection(
    host=hostname,
    port=port,
    user=user,
    password=password
)

# ------------------------------------------
# Crear base de datos si no existe
# ------------------------------------------

# Crea un cursor para ejecutar comandos SQL sobre la conexión establecida
cursor = db.cursor()

# Ejecuta una instrucción SQL para crear la base de datos 'books_db' solo si no existe previamente
cursor.execute("CREATE DATABASE IF NOT EXISTS books_db")

# Ejecuta una consulta para obtener todas las bases de datos disponibles en el servidor
cursor.execute("SHOW DATABASES")

# Itera sobre el resultado de la consulta y muestra cada base de datos encontrada
for database in cursor:
    print(database)

# ------------------------------------------
# Cierre de conexión
# ------------------------------------------

# Cierra el cursor para liberar recursos asociados a él
cursor.close()

# Cierra la conexión a MySQL
db.close()
