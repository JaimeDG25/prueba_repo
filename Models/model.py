from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()
class Usuario(db.Model):
    __tablename__ = 'usuario'
    id_usuario = db.Column(db.Integer, primary_key=True,autoincrement=True)
    nombre_usuario = db.Column(db.String(100), nullable=False)
    correo_usuario = db.Column(db.String(150), nullable=False)
    contraseña_usuario = db.Column(db.String(130), nullable=False)
    fcreacion_usuario = db.Column(db.DateTime, default=datetime.utcnow)
    
class Cotizaciones(db.Model):
    __tablename__ = 'cotizacion'
    id_cotizacion = db.Column(db.Integer, primary_key=True,autoincrement=True)
    numero_cotizacion = db.Column(db.String(100), nullable=False)
    nombrecliente_cotizacion = db.Column(db.String(100), nullable=False)
    correocliente_cotizacion = db.Column(db.String(100), nullable=False)
    tservicio_cotizacion = db.Column(db.String(100), nullable=False)
    precio_cotizacion = db.Column(db.Integer)
    fcreacion_cotizacion = db.Column(db.DateTime, default=datetime.utcnow)
