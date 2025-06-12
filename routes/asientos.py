from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Asiento(db.Model):
    __tablename__ = 'asientos'
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(5), nullable=False)  # Ej: A1, B1
    tour_id = db.Column(db.Integer, db.ForeignKey('tours.id'), nullable=False)
    reservado = db.Column(db.Boolean, default=False)
    reserva_id = db.Column(db.Integer, db.ForeignKey('reservas.id'), nullable=True)

    def __repr__(self):
        return f"<Asiento {self.numero} - Reservado: {self.reservado}>"
