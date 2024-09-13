from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "knoworld_secret"

# Simulamos una base de datos en memoria
users = {}
friend_requests = {}
messages = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in users and users[email]['password'] == password:
            return redirect(url_for('home', email=email))
        else:
            flash('Correo o contraseña incorrectos.')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in users:
            flash('El correo ya está registrado.')
        else:
            users[email] = {'password': password, 'friends': []}
            flash('Registro exitoso, ahora puedes iniciar sesión.')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/home/<email>')
def home(email):
    user_friends = users[email]['friends']
    return render_template('home.html', email=email, friends=user_friends)

@app.route('/add_friend/<email>', methods=['POST'])
def add_friend(email):
    friend_email = request.form['friend_email']
    if friend_email in users and friend_email != email:
        if friend_email not in friend_requests:
            friend_requests[friend_email] = []
        friend_requests[friend_email].append(email)
        flash('Solicitud de amistad enviada.')
    else:
        flash('Usuario no encontrado.')
    return redirect(url_for('home', email=email))

@app.route('/send_message/<email>', methods=['POST'])
def send_message(email):
    friend_email = request.form['friend_email']
    message_text = request.form['message']
    
    if friend_email in users:
        if friend_email not in messages:
            messages[friend_email] = []
        messages[friend_email].append(f"{email}: {message_text}")
        flash('Mensaje enviado.')
    else:
        flash('Usuario no encontrado.')
    
    return redirect(url_for('home', email=email))

if __name__ == '__main__':
    app.run(debug=True)
