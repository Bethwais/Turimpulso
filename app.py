from flask import Flask, render_template, Blueprint, request, redirect, url_for, flash, session
from flask_dance.contrib.google import make_google_blueprint, google
import os
from routes.reservas import reservas_bp
from routes.pagos import pagos_bp

app = Flask(__name__)

# Clave secreta para Flask (cámbiala en producción)
app.secret_key = os.environ.get('SECRET_KEY', 'clave_secreta_para_desarrollo')

# Configurar Google OAuth con Flask-Dance
google_bp = make_google_blueprint(
    client_id=os.environ.get("GOOGLE_CLIENT_ID", ""),
    client_secret=os.environ.get("GOOGLE_CLIENT_SECRET", ""),
    scope=["profile", "email"],
    redirect_url="http://localhost:5000/google_login/callback"  # Cambia a producción
)
app.register_blueprint(google_bp, url_prefix="/login")

# Registrar blueprints de rutas
app.register_blueprint(reservas_bp, url_prefix='/reservas')
app.register_blueprint(pagos_bp, url_prefix='/pagos')

# Blueprint para contacto
contacto_bp = Blueprint('contacto', __name__)

@contacto_bp.route('/contacto', methods=['GET'])
def contacto():
    return render_template('contacto.html')

@contacto_bp.route('/contacto', methods=['POST'])
def enviar_mensaje():
    nombre = request.form.get('nombre')
    email = request.form.get('email')
    mensaje = request.form.get('mensaje')
    asunto = request.form.get('asunto', '')
    # Aquí puedes procesar el mensaje (guardar o enviar email)
    flash('¡Mensaje enviado con éxito!', 'success')
    return redirect(url_for('contacto.contacto'))

app.register_blueprint(contacto_bp)

# Rutas principales
@app.route('/')
def inicio():
    return render_template('inicio.html')

@app.route('/tours')
def tours():
    return render_template('tours.html')

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

# Callback para Google OAuth
@app.route("/google_login/callback")
def google_login_callback():
    if not google.authorized:
        return redirect(url_for("google.login"))

    resp = google.get("/oauth2/v2/userinfo")
    if not resp.ok:
        flash("No se pudo obtener la información de Google.", "error")
        return redirect(url_for("inicio"))

    info = resp.json()
    session['usuario'] = {
        "nombre": info.get("name"),
        "email": info.get("email")
    }

    # Si había una reserva en sesión, actualizar el email
    if 'reserva' in session:
        session['reserva']['email'] = info.get("email")

    flash(f"Bienvenido, {info.get('name')}!", "success")
    return redirect(url_for("inicio"))

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    session.pop('usuario', None)
    flash("Has cerrado sesión.", "info")
    return redirect(url_for("inicio"))

# Ruta para crear reserva de prueba
@app.route('/crear_reserva_prueba')
def crear_reserva_prueba():
    session['reserva'] = {
        'nombre': 'Luis',
        'email': 'luis@example.com',
        'tour': 'cultural-cdmx',
        'personas': '2'  # Coincidir con pagos.py
    }
    flash("Reserva de prueba creada.", "info")
    return redirect(url_for('pagos.pagar'))

if __name__ == '__main__':
    app.run(debug=True)
