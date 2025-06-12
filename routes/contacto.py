from flask import Blueprint, render_template, request, redirect, url_for, flash

contacto_bp = Blueprint('contacto', __name__)

@contacto_bp.route('/contacto', methods=['GET'])
def contacto():
    return render_template('contacto.html')

@contacto_bp.route('/contacto/enviar_mensaje', methods=['POST'])
def enviar_mensaje():
    nombre = request.form.get('nombre')
    email = request.form.get('email')
    asunto = request.form.get('asunto')
    mensaje = request.form.get('mensaje')

    flash(f"Gracias {nombre}, hemos recibido tu mensaje.", "success")

    return redirect(url_for('contacto.contacto'))
