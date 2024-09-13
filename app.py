from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, send
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///knoworld.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
db = SQLAlchemy(app)
socketio = SocketIO(app)

# Modelo de Usuario
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    profile_pic = db.Column(db.String(100), default='default.jpg')
    cover_pic = db.Column(db.String(100), default='default_cover.jpg')

# Modelo de Estado (Post)
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# Modelo de Solicitudes de Amistad
class FriendRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    to_user = db.Column(db.Integer, db.ForeignKey('user.id'))

# Página de inicio
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('profile', user_id=session['user_id']))
    return render_template('index.html')

# Página de registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        session['user_id'] = user.id
        return redirect(url_for('profile', user_id=user.id))
    return render_template('register.html')

# Página de perfil
@app.route('/profile/<int:user_id>')
def profile(user_id):
    user = User.query.get(user_id)
    return render_template('profile.html', user=user)

# Subir foto de perfil
@app.route('/upload_profile_pic', methods=['POST'])
def upload_profile_pic():
    file = request.files['profile_pic']
    if file:
        filename = f"profile_{session['user_id']}.jpg"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        user = User.query.get(session['user_id'])
        user.profile_pic = filename
        db.session.commit()
    return redirect(url_for('profile', user_id=session['user_id']))

# Funcionalidad del Chat
@app.route('/chat')
def chat():
    return render_template('chat.html')

# Envío de mensajes de chat en tiempo real
@socketio.on('message')
def handleMessage(msg):
    send(msg, broadcast=True)

# Cerrar sesión
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()
    socketio.run(app, debug=True)
