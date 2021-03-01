from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
class Favoritos(db.Model):
    __tablename__ = 'favoritos'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    personajes_name = db.Column(db.String(250), db.ForeignKey('personajes.name'))
    planetas_name = db.Column(db.String(250), db.ForeignKey('planetas.name'))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "personajes_name": self.personajes_name,
            "planetas_name": self.planetas_name
            # do not serialize the password, its a security breach
        }


class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    contraseña = db.Column(db.String(20)) 
    name = db.Column(db.String(250))

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            # do not serialize the password, its a security breach
        }

class Personajes(db.Model):
    __tablename__ = 'personajes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250),unique=True)
    estatura = db.Column(db.String(250))
    fecha_nacimiento = db.Column(db.String(250))
    genero = db.Column(db.String(250))
    favoritoP = db.relationship('Favoritos')
    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "estatura": self.estatura,
            "fecha_nacimiento": self.fecha_nacimiento,
            "genero": self.genero,
            # do not serialize the password, its a security breach
        }

class Planetas(db.Model):
    __tablename__ = 'planetas'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250),unique=True)
    poblacion = db.Column(db.Integer)
    diametro = db.Column(db.Integer)
    gravedad = db.Column(db.String(250))
    favorito = db.relationship('Favoritos')

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "poblacion": self.poblacion,
            "diametro": self.diametro,
            "gravedad": self.gravedad,
            # do not serialize the password, its a security breach
        }

