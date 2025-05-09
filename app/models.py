from . import db  # Importa la instancia 'db' de SQLAlchemy desde app/__init__.py
import datetime   # Para el campo de fecha en el modelo Voto

class Bar(db.Model):
    __tablename__ = 'bares'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    direccion = db.Column(db.String(200), nullable=True)
    votos = db.relationship('Voto', backref='bar_votado_obj', lazy='dynamic') # 'dynamic' para consultas más grandes

    def __repr__(self):
        return f'<Bar {self.nombre}>'

class CategoriaPintxo(db.Model):
    __tablename__ = 'categorias_pintxos'
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(50), nullable=False, unique=True) # ej: "tortilla", "creativo"
    nombre_visible = db.Column(db.String(100), nullable=False) # ej: "Tortilla de Patatas"
    votos = db.relationship('Voto', backref='categoria_votada_obj', lazy='dynamic')

    def __repr__(self):
        return f'<CategoriaPintxo {self.nombre_visible}>'

class Votante(db.Model):
    __tablename__ = 'votantes'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    votos = db.relationship('Voto', backref='votante_obj', lazy='dynamic')

    def __repr__(self):
        return f'<Votante {self.email}>'

class Voto(db.Model):
    __tablename__ = 'votos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    votante_id = db.Column(db.Integer, db.ForeignKey('votantes.id'), nullable=False)
    bar_id = db.Column(db.Integer, db.ForeignKey('bares.id'), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias_pintxos.id'), nullable=False)
    fecha_voto = db.Column(db.DateTime, nullable=False, default=lambda: datetime.datetime.now(timezone.utc))

    # Añadir esto para la restricción de unicidad
    __table_args__ = (db.UniqueConstraint('votante_id', 'categoria_id', name='uq_votante_categoria_unica'),)

    def __repr__(self):
        return f'<Voto {self.id}>'