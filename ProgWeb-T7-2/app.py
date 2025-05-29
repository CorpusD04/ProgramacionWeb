# Importamos las clases y funciones necesarias desde Flask
from flask import Flask, request, redirect, url_for, render_template
# Importamos SQLAlchemy para manejar la base de datos ORM
from flask_sqlalchemy import SQLAlchemy

# Inicializamos la aplicación Flask
app = Flask(__name__)

# Configuramos la URI de conexión con la base de datos MySQL
# Usamos pymysql como driver, la base de datos está en localhost puerto 3307, con usuario root y contraseña fairy15
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:fairy15@localhost:3307/books_db'

# Desactivamos la característica que hace seguimiento de modificaciones en los objetos SQLAlchemy para evitar advertencias y mejorar rendimiento
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Creamos la instancia de SQLAlchemy vinculada a la app Flask
db = SQLAlchemy(app)

# Definimos el modelo Book que representa la tabla 'books' en la base de datos
class Book(db.Model):
    __tablename__ = 'books'  # Nombre explícito de la tabla en la BD
    id = db.Column(db.Integer, primary_key=True)  # Columna 'id' como clave primaria y autoincremental
    title = db.Column(db.String(100), nullable=False)  # Columna 'title' que guarda el título del libro, no puede ser nula
    author = db.Column(db.String(50), nullable=False)  # Columna 'author' para el autor del libro, no puede ser nula
    genre = db.Column(db.String(20), nullable=False)  # Columna 'genre' para el género literario, no puede ser nula

    # Constructor para crear objetos Book fácilmente con título, autor y género
    def __init__(self, title, author, genre):
        self.title = title
        self.author = author
        self.genre = genre

    # Representación en texto del objeto Book para debugging
    def __repr__(self):
        return f'<Book {self.title}>'

# Ruta principal '/' que muestra la lista de libros y el formulario para agregar uno nuevo
@app.route('/')
def index():
    # Consulta todos los libros de la base de datos
    books = Book.query.all()
    # Renderiza el template 'index.html' enviándole la lista de libros para mostrar
    return render_template('index.html', books=books)

# Ruta '/books' que maneja la creación de un libro nuevo vía formulario HTML (método POST)
@app.route('/books', methods=['POST'])
def add_book():
    # Obtiene los datos enviados desde el formulario con el método POST
    title = request.form.get('title')    # Extrae el título del libro del formulario
    author = request.form.get('author')  # Extrae el autor del libro
    genre = request.form.get('genre')    # Extrae el género literario

    # Crea un nuevo objeto Book con los datos recibidos
    new_book = Book(title=title, author=author, genre=genre)

    # Agrega el nuevo libro a la sesión de la base de datos para luego guardarlo
    db.session.add(new_book)
    # Confirma la transacción guardando el nuevo libro en la base de datos
    db.session.commit()

    # Redirige al usuario de vuelta a la página principal para ver la lista actualizada
    return redirect(url_for('index'))

# Ruta para editar un libro existente, recibe el ID del libro a editar
# Permite GET para mostrar formulario con datos actuales y POST para actualizar el libro
@app.route('/books/<int:id>/edit', methods=['GET', 'POST'])
def edit_book(id):
    # Busca el libro por su ID o devuelve error 404 si no existe
    book = Book.query.get_or_404(id)

    if request.method == 'POST':
        # Si se envió el formulario (POST), actualizamos los campos con los nuevos datos
        book.title = request.form.get('title')
        book.author = request.form.get('author')
        book.genre = request.form.get('genre')

        # Guardamos los cambios en la base de datos
        db.session.commit()

        # Redirigimos a la página principal para ver la lista actualizada
        return redirect(url_for('index'))

    # Si la petición es GET, renderizamos el formulario de edición con los datos actuales del libro
    return render_template('edit.html', book=book)

# Ruta para eliminar un libro, recibe el ID del libro a eliminar
@app.route('/books/<int:id>/delete', methods=['GET'])
def delete_book(id):
    # Busca el libro por su ID o devuelve error 404 si no existe
    book = Book.query.get_or_404(id)

    # Elimina el libro de la sesión
    db.session.delete(book)
    # Confirma la eliminación en la base de datos
    db.session.commit()

    # Redirige a la página principal para ver la lista actualizada sin el libro eliminado
    return redirect(url_for('index'))

# Esta condición asegura que este archivo se ejecute directamente
if __name__ == '__main__':
    # Crea las tablas de la base de datos si no existen (dentro del contexto de la app)
    with app.app_context():
        db.create_all()
    # Inicia el servidor Flask en modo debug para facilitar desarrollo
    app.run(debug=True)
