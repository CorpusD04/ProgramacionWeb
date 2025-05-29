# Importa el módulo pymysql, que permite conectar y ejecutar consultas sobre una base de datos MySQL desde Python
import pymysql

# ------------------------------------------
# Conexión a la base de datos MySQL
# ------------------------------------------

# Establece la conexión con la base de datos 'books_db' usando pymysql.connect().
# Parámetros:
#   host     : dirección del servidor de base de datos, en este caso 'localhost' (equivale a 127.0.0.1).
#   port     : puerto 3307 (el puerto por defecto de MySQL suele ser 3306)
#   user     : nombre de usuario de la base de datos, aquí es 'root'.
#   password : contraseña del usuario. 
#   database : nombre de la base de datos a la que se desea conectar, en este caso 'books_db'.
db = pymysql.connect(
    host='localhost',
    port=3307,
    user='root',
    password='fairy15',  
    database='books_db'
)

# Crea un cursor que se usa para ejecutar comandos SQL en la base de datos conectada.
cursor = db.cursor()

# Ejecuta una consulta SQL que lista todas las tablas presentes en la base de datos actual ('books_db').
cursor.execute("SHOW TABLES")

# Imprime un encabezado para mostrar las tablas listadas.
print("Tablas en la base de datos 'books_db':")

# Itera sobre los resultados devueltos por el cursor.
# Cada fila representa una tabla de la base de datos. Se imprime cada una de ellas.
for table in cursor:
    print(table)

# Cierra el cursor, liberando los recursos asociados a él.
cursor.close()

# Cierra la conexión a la base de datos, terminando la sesión actual.
db.close()
