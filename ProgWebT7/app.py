from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)  # Se inicializa la aplicación Flask

# Configuración de la conexión a MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3307
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'fairy15'
app.config['MYSQL_DB'] = 'tarea7PW'
mysql = MySQL(app)  # Se asocia la configuración de MySQL a la app

"""
# Aquí comienza el bloque seguro con contexto
with app.app_context():
    # Crear cursor y ejecutar comandos SQL dentro del contexto de Flask
    cursor = mysql.connection.cursor()
    
    # Ejecutar sentencias SQL (ajusta los nombres de tabla/campos)
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(100),
                        email VARCHAR(100))''')

    # Ejemplo: insertar un usuario 
    cursor.execute('''INSERT INTO users (name, email) VALUES (%s, %s)''', ('Ejemplo', 'ejemplo@mail.com'))

    # Guardar los cambios
    mysql.connection.commit()

    # Cerrar el cursor
    cursor.close()
"""
@app.route('/')
def form():
    return render_template('index.html')
 
@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'GET':
        return "Login via the login Form"
     
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        cursor = mysql.connection.cursor()
        cursor.execute(''' INSERT INTO users (name, email) VALUES(%s,%s)''',(name,email))
        mysql.connection.commit()
        cursor.close()
        return f"Done!!"
 
app.run(host='localhost', port=5000)