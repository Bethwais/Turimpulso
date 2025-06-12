from flask import Blueprint, render_template, redirect, url_for, session, request
from datetime import datetime

reservas_bp = Blueprint('reservas', __name__, url_prefix='/reservas')

@reservas_bp.route('/', methods=['GET', 'POST'])
def reservas():
    mensaje = None
    exito = None
    datos = None

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        fecha = request.form.get('fecha')
        tour = request.form.get('tour')
        turno = request.form.get('turno')
        horario = request.form.get('horario')
        asientos_str = request.form.get('asientosSeleccionados')  # Ej: "1,3,4"

        # Guardar datos enviados para mantener en formulario en caso de error
        datos = request.form

        # Validación básica
        if not nombre or not email or not fecha or not tour or not turno or not horario or not asientos_str:
            mensaje = "Por favor completa todos los campos obligatorios."
            return render_template('reservas.html', mensaje=mensaje, exito=None, datos=datos, now=datetime.now(), tour=tour)

        # Validar formato y fecha (fecha no pasada)
        try:
            fecha_viaje = datetime.strptime(fecha, "%Y-%m-%d").date()
            if fecha_viaje < datetime.now().date():
                mensaje = "La fecha del viaje no puede ser anterior a hoy."
                return render_template('reservas.html', mensaje=mensaje, exito=None, datos=datos, now=datetime.now(), tour=tour)
        except ValueError:
            mensaje = "Fecha inválida."
            return render_template('reservas.html', mensaje=mensaje, exito=None, datos=datos, now=datetime.now(), tour=tour)

        asientos_lista = [int(a) for a in asientos_str.split(',') if a.isdigit()]
        cantidad_personas = len(asientos_lista)

        if cantidad_personas == 0:
            mensaje = "Debes seleccionar al menos un asiento."
            return render_template('reservas.html', mensaje=mensaje, exito=None, datos=datos, now=datetime.now(), tour=tour)

        # Precios base según tour (puedes ajustar)
        precios = {
            'cultural-cdmx': 1200,
            'aventura-chiapas': 2200,
            'gastronomia-oaxaca': 1500,
            'selva-lacandona': 2300,
            'historico-guanajuato': 1300,
            'arqueologico-teotihuacan': 1400,
            'colonial-san-miguel': 1600,
            'cenotes-yucatan': 1800
        }

        precio_por_persona = precios.get(tour, 1000)  # fallback 1000
        total = cantidad_personas * precio_por_persona

        # Guardar reserva en sesión
        session['reserva'] = {
            'nombre': nombre,
            'email': email,
            'fecha': fecha,
            'tour': tour,
            'turno': turno,
            'horario': horario,
            'personas': cantidad_personas,
            'asientos': asientos_lista,
            'total': total
        }

        exito = f"Reserva registrada exitosamente. Total a pagar: MXN ${total}"
        return redirect(url_for('reservas.confirmar_reserva'))

    # GET
    tour = request.args.get('tour')
    return render_template('reservas.html', mensaje=None, exito=None, datos=None, now=datetime.now(), tour=tour)


@reservas_bp.route('/confirmar', methods=['GET'])
def confirmar_reserva():
    reserva = session.get('reserva')
    if not reserva:
        return redirect(url_for('reservas.reservas'))
    return render_template('confirmar_reserva.html', reserva=reserva)


@reservas_bp.route('/cancelar', methods=['GET'])
def cancelar_reserva():
    session.pop('reserva', None)
    return redirect(url_for('reservas.reservas'))


@reservas_bp.route('/terminar/<string:destino>', methods=['GET'])
def terminar_reserva(destino):
    session.pop('reserva', None)
    destinos_validos = {
        'inicio': 'reservas.reservas',
        'exito': 'pagos.exito',
        'cancelado': 'pagos.cancelado'
    }
    ruta = destinos_validos.get(destino)
    if ruta:
        return redirect(url_for(ruta))
    return redirect(url_for('reservas.reservas'))  