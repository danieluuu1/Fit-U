# backend/app.py

from flask import Flask, render_template
from dotenv import load_dotenv, find_dotenv
import os

# Carga .env
print("CWD app.py:", os.getcwd())
dotenv_path = find_dotenv()
print("DOTENV PATH app.py:", dotenv_path)
load_dotenv(dotenv_path)

# Calcula rutas absolutas para frontend
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'frontend', 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'frontend', 'static')

# Inicializa Flask con carpetas personalizadas
app = Flask(
    __name__,
    template_folder=TEMPLATES_DIR,
    static_folder=STATIC_DIR,
    static_url_path='/static'
)

# Importa y registra los blueprints
from routes.auth_routes import auth_bp
from routes.routine_routes import routine_bp
app.register_blueprint(auth_bp)
app.register_blueprint(routine_bp)

# Rutas de vistas
@app.route('/register')
def show_register():
    return render_template('register.html')

@app.route('/login')
def show_login():
    return render_template('login.html')

@app.route('/routine')
def show_routine_form():
    return render_template('routine.html')

@app.route('/dashboard')
def dashboard():
    return "<h2>Bienvenido al Dashboard</h2>"

if __name__ == '__main__':
    app.run(debug=True)
