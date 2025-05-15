from . import db  # Importa la instancia 'db' de SQLAlchemy desde app/__init__.py
import datetime   # Para el campo de fecha en el modelo Voto
from datetime import timezone # Para la fecha UTC correcta
from sqlalchemy.sql import func 

class Rol(db.Model):
    __tablename__ = 'roles'
    id_rol = db.Column(db.Integer, primary_key=True)
    rol = db.Column(db.String(50), nullable=False, unique=True)
    usuarios = db.relationship('Usuario', backref='rol_obj', lazy='dynamic')

    def __repr__(self):
        return f'<Rol {self.rol}>'

class Usuario(db.Model): 
    __tablename__ = 'usuarios'
    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(100), nullable=False)
    email_usuario = db.Column(db.String(100), nullable=False, unique=True)
    pass_usuario = db.Column(db.String(45), nullable=False) # sin hashear por ahora
    estado_usuario = db.Column(db.Enum('activo','inactivo','pendiente'), default='activo')
    id_rol = db.Column(db.Integer, db.ForeignKey('roles.id_rol'), nullable=False)
    
    votos = db.relationship('Voto', backref='usuario_obj', lazy='dynamic')

    def __repr__(self):
        return f'<Usuario {self.email_usuario}>'

class Bar(db.Model):
    __tablename__ = 'bares'
    id_bar = db.Column(db.Integer, primary_key=True)
    nombre_bar = db.Column(db.String(100), nullable=False) # El dump lo tiene unique indirectamente por los pintxos, pero no en la tabla. Considerar unique=True
    direccion = db.Column(db.String(150), nullable=False) # El dump dice NOT NULL
    
    pintxos = db.relationship('Pintxo', backref='bar_obj', lazy='dynamic')

    def __repr__(self):
        return f'<Bar {self.nombre_bar}>'

class Categoria(db.Model): 
    __tablename__ = 'categorias'
    id_categoria = db.Column(db.Integer, primary_key=True)
    nombre_categoria = db.Column(db.String(50), nullable=False) # Este sería el nombre visible y también el "slug" implícito
    
    pintxos = db.relationship('Pintxo', backref='categoria_obj', lazy='dynamic')

    def __repr__(self):
        return f'<Categoria {self.nombre_categoria}>'

class Pintxo(db.Model):
    __tablename__ = 'pintxos'
    id_pintxo = db.Column(db.Integer, primary_key=True)
    nombre_pintxo = db.Column(db.String(100), nullable=False)
    id_categoria = db.Column(db.Integer, db.ForeignKey('categorias.id_categoria'), nullable=False)
    id_bar = db.Column(db.Integer, db.ForeignKey('bares.id_bar'), nullable=False)
    
    votos = db.relationship('Voto', backref='pintxo_obj', lazy='dynamic')

    def __repr__(self):
        return f'<Pintxo {self.nombre_pintxo}>'

class Voto(db.Model):
    __tablename__ = 'votos'
    id_voto = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    id_pintxo = db.Column(db.Integer, db.ForeignKey('pintxos.id_pintxo'), nullable=False)
    # El dump usa DEFAULT current_timestamp(). SQLAlchemy puede manejar esto.
    fecha_voto = db.Column(db.DateTime, nullable=False, server_default=func.now()) # o db.func.current_timestamp()

    # --- NUEVO CAMPO ---
    id_categoria = db.Column(db.Integer, db.ForeignKey('categorias.id_categoria'), nullable=False)

    # --- RESTRICCIÓN DE UNICIDAD MODIFICADA ---
    # Un usuario puede votar solo una vez POR CATEGORÍA.
    # El nombre 'unique_voto_por_categoria' es más descriptivo.
    # La definición SQL tiene dos UNIQUE KEY que parecen ser para (id_usuario, id_categoria),
    # 'id_usuario' y 'unique_voto_por_categoria'. En SQLAlchemy definimos una con el nombre más claro.
    __table_args__ = (
        db.UniqueConstraint('id_usuario', 'id_categoria', name='uq_usuario_categoria_unica'),
    )

    def __repr__(self):
        return f'<Voto {self.id_voto} - Usuario: {self.id_usuario} Pintxo: {self.id_pintxo} Categoria: {self.id_categoria}>'

