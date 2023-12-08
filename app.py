from flask import Flask, render_template, request, make_response,session,escape,redirect,url_for,Blueprint,flash,json
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
dbdir = "sqlite:///" + os.path.abspath(os.getcwd()) + "/base.db"
app.config["SQLALCHEMY_DATABASE_URI"] = dbdir
app.config['SECRET_KEY'] = 'secret_key'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Persona(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    apellido = db.Column(db.String(80), nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    numero = db.Column(db.String(15), nullable=False)
    sexo = db.Column(db.String(10), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
    
        # Verifica si el usuario ya existe en la base de datos
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return render_template('vista2.html', show_alert=True)

        # Crea una instancia del usuario y guarda en la base de datos
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return render_template('vista2.html', show_alert2=True)

    return render_template('vista2.html', show_alert=False, show_alert2=False)


@app.route('/login/select', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Verifica si el usuario existe en la base de datos
        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            return render_template('vista3.html', show_alert=True)
        session['username'] = username
        resp = make_response("Inicio de sesión exitoso")
        resp.set_cookie('username', username)  # Establecer cookie con el nombre de usuario
        return render_template('inicio.html', show_alert2=True)
    return render_template('vista3.html', show_alert=False, show_alert2=False)

@app.route('/logout')
def logout():
    # Elimina la información de la sesión y la cookie del nombre de usuario
    session.pop('username', None)
    resp = make_response("Cerrar sesión exitoso")
    resp.set_cookie('username', '', expires=0)  # Elimina la cookie del nombre de usuario
    return render_template('index.html') 

@app.route('/cookie/read')
def read_cookie():
    username = request.cookies.get('username', None)
    return username


@app.route('/iniciar_sesion')
def iniciar_sesion():
    if 'username' in session:
        return "Tu eres: %s" % escape(session['username'])
    return "Debes Iniciar Sesión"

@app.route('/ver')
def ver():
    personas = Persona.query.all()
    return render_template('ver.html', personas=personas, show_alert2=True)

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    persona = Persona.query.get(id)
    
    if request.method == 'POST':
        persona.nombre = request.form['nombre']
        persona.apellido = request.form['apellido']
        persona.correo = request.form['correo']
        persona.numero = request.form['numero']
        persona.sexo = request.form['sexo']
        db.session.commit()
        return redirect(url_for('ver'))
    
    return render_template('editar.html', persona=persona)

@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        correo = request.form['correo']
        numero = request.form['numero']
        sexo = request.form['sexo']
        nueva_persona = Persona(nombre=nombre, apellido=apellido, correo=correo, numero=numero, sexo=sexo)
        db.session.add(nueva_persona)
        db.session.commit()
        return redirect(url_for('ver'))
    
    return render_template('agregar.html')

@app.route('/eliminar/<int:id>')
def eliminar(id):
    persona = Persona.query.get(id)
    db.session.delete(persona)
    db.session.commit()
    return redirect(url_for('ver'))

@app.route('/eliminar/<int:id>/confirmar', methods=['GET', 'POST'])
def eliminar_confirmar(id):
    persona = Persona.query.get(id)
    db.session.delete(persona)
    db.session.commit()
    return redirect(url_for('ver'))
    
    #return render_template('eliminar.html', persona=persona)


if __name__ == "__main__":
    app.run(debug=True)
    