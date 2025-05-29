from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__) #Se inicializa la aplicación Flask.

# Configuración de la conexión a MySQL
mysql = MySQL()
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3307
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'fairy15'
app.config['MYSQL_DB'] = 'tarea6PW'
mysql.init_app(app) #init_app() asocia la configuración de MySQL a la app Flask.

# RUTA PRINCIPAL (READ)
@app.route('/')  #Ruta raíz '/': muestra todos los registros de la tabla users.
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users") #Abre un cursor, ejecuta un SELECT * para obtener todos los usuarios.
    data = cur.fetchall()
    #Cierra el cursor y pasa los datos a index.html para mostrarlos.
    cur.close()
    return render_template('index.html', users=data) 

# RUTA PARA AGREGAR (CREATE)
@app.route('/add', methods=['POST']) #Ruta /add: se activa cuando se envía el formulario para agregar un nuevo usuario
def add_user():
    #Obtiene los datos del formulario HTML (name, email).
    name = request.form['name']
    email = request.form['email']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
    mysql.connection.commit()
    return redirect(url_for('index')) #Redirige de nuevo a la página principal.

# RUTA PARA ELIMINAR (DELETE)
@app.route('/delete/<int:id>') #Ruta /delete/<id>: recibe un ID desde la URL.
def delete_user(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id = %s", (id,)) #Ejecuta un DELETE sobre el usuario con ese ID.
    mysql.connection.commit()
    return redirect(url_for('index')) #Después, redirige a la página principal.

# RUTA PARA EDITAR (UPDATE - MOSTRAR FORMULARIO)
@app.route('/edit/<int:id>') #Ruta /edit/<id>: muestra el formulario con los datos actuales del usuario
def edit_user(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s", (id,)) #Realiza un SELECT del usuario por ID.
    user = cur.fetchone()
    return render_template('edit.html', user=user) #Muestra el formulario (edit.html) con esos datos precargados.

# RUTA PARA ACTUALIZAR (UPDATE - GUARDAR CAMBIOS)
@app.route('/update/<int:id>', methods=['POST']) #Ruta /update/<id>: se activa cuando el usuario guarda los 
                                                    #cambios del formulario de edición.
def update_user(id):
    #Recupera los datos nuevos (name, email) desde el formulario.
    name = request.form['name']
    email = request.form['email']
    cur = mysql.connection.cursor()
    #Ejecuta un UPDATE sobre el usuario con el ID correspondiente
    cur.execute("UPDATE users SET name = %s, email = %s WHERE id = %s", (name, email, id)) 
    mysql.connection.commit()
    return redirect(url_for('index')) #Redirige al listado principal.

if __name__ == '__main__':
    #Ejecuta el servidor Flask con debug=True para recargar automáticamente y mostrar errores detallados.
    app.run(debug=True)
