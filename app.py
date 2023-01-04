from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from flask_bcrypt import Bcrypt
from flask_login import LoginManager,login_user, current_user, logout_user, login_required, UserMixin
from dotenv import load_dotenv
import os


# Cargar las variables de entorno que se encuentran en .env
load_dotenv('.env')

# Instancia de la app
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')


app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

db = SQLAlchemy()

# Instancia para hashear contraseñas
bcrypt = Bcrypt(app)


# Clases para crear la tabla de usuarios y tareas

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), unique=True)
    password = db.Column(db.String(40))
    todo_id = db.relationship('Todo', backref="owner_task", lazy=True)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(144))
    complete = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)

#-----------------  FORMULARIOS ------------------------------

# Formulario para crear tarea
class TodoForm(FlaskForm):
    content = StringField('Tarea', validators=[DataRequired(), Length(min=2, max=144)])
    complete = BooleanField()
    submit = SubmitField('Agregar')

# Actualizar tarea
class UpdateForm(FlaskForm):
    content = StringField('Tarea', validators=[DataRequired()])
    submit = SubmitField('Actualizar')

# Registro de usuarios
class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired(),
                                                       Regexp(
            r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$',
            message='La contraseña debe tener al menos 6 caracteres y contener al menos una letra mayúscula, una minúscula, un símbolo y un número'
        )])
    confirm_password= PasswordField('Confirmar contraseña', validators=[DataRequired(), EqualTo('password')])
    submit= SubmitField('Registrarse')
    
    # Funcion para validar email y que no haya dos repetidos en la base de datos
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

# Inicio de sesion
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar sesion')


# Creacion de tablas en base de datos

db.init_app(app)
with app.app_context():
    db.create_all()
    
# Instancia de LoginManager
login_manager = LoginManager()

login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



# Handlers

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', error=error), 404


@app.errorhandler(500)
def page_not_found(error):
    return render_template('500.html',error=error), 500



#------------------------------    RUTAS     -------------------------------------------

# Ruta para crear tarea

@app.route('/', methods=['GET', 'POST'])
@login_required
def add():
    #formulario
    form = TodoForm()
    # Consulta para obtener las tareas completas e incompletas
    incomplete = Todo.query.filter_by(complete=False, user_id=current_user.id).all()
    completed = Todo.query.filter_by(complete=True, user_id=current_user.id).all()
    # Si el formulario es valido
    if form.validate_on_submit():
        # Crea tarea
        todo = Todo(text=form.content.data, complete=False, user_id= current_user.id)
        # Se agrega a base de datos
        db.session.add(todo)
        # Compromete los cambios
        db.session.commit()
        return redirect(url_for('add'))
    return render_template('index.html',form=form, incomplete=incomplete, completed=completed)


# Ruta para actualizar tarea

@app.route('/edit/<int:id>', methods=['GET','POST'])
@login_required
def edit(id):
    todo = Todo.query.get(id)
    form = UpdateForm()
    
    # Verificar que la tarea existe y pertenece al usuario loggeado, sino aborta
    if current_user.id != todo.user_id:
        abort(404)
    
    if form.validate_on_submit():
        todo.text = form.content.data
        db.session.commit()
        return redirect(url_for('add'))
    elif request.method == 'GET':
        form.content.data = todo.text
    return render_template('edit.html', todo=todo, form=form)


# Ruta para eliminar tarea

@app.route('/delete/<int:id>', methods=['GET','POST'])
@login_required
def delete(id):
    todo = Todo.query.get_or_404(id)
    if current_user.id != todo.user_id:
        abort(404)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('add'))
    
# Ruta para marcar tarea completa

@app.route('/completed/<int:id>', methods=['GET','POST'])
@login_required
def completed(id):
    
    todo = Todo.query.get_or_404(id)
    if current_user.id != todo.user_id:
        abort(404)
    todo.complete = True
    db.session.commit()
    return redirect(url_for('add'))


# Ruta para marcar tarea incompleta

@app.route('/incompleted/<int:id>', methods=['GET','POST'])
@login_required
def incompleted(id):
    todo = Todo.query.get_or_404(id)
    
    if current_user.id != todo.user_id:
        abort(404)
    todo.complete = False
    db.session.commit()
    return redirect(url_for('add'))
    

# Ruta para registrarse

@app.route('/register', methods=['GET','POST'])
def register():
    # Si el usuario ya esta loggeado, no podra ingresar a esta ruta
    if current_user.is_authenticated:
        return redirect(url_for('add'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Tu cuenta ha sido creada con exito, ya puedes iniciar sesion!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


# Ruta para iniciar sesion

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('add'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('add'))
        flash('Inicio de sesion fallido, verifique su email')
    return render_template('login.html', form=form)

# Ruta para cerrar sesion

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))
                




if __name__ == '__main__':
    app.run()
