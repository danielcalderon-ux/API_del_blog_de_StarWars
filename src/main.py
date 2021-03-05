"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Usuario, Personajes, Planetas, Favoritos
#from models import Person

## Nos permite hacer las encripciones de contraseñas
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():
    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/usuarios', methods=['GET'])
def get_usuario():
    usuario_query = Usuario.query.all()
    all_usuarios = list(map(lambda x: x.serialize(), usuario_query))
    return jsonify(all_usuarios), 200

@app.route('/personajes', methods=['GET'])
def get_personajes():
    personajes_query = Personajes.query.all()
    all_personajes = list(map(lambda x: x.serialize(), personajes_query))
    return jsonify(all_personajes), 200

@app.route('/planetas', methods=['GET'])
def get_planetas():
    planetas_query = Planetas.query.all()
    all_planetas = list(map(lambda x: x.serialize(), planetas_query))
    return jsonify(all_planetas), 200

@app.route('/personajes/<int:id>', methods=['GET'])
def get_personaje(id):
    personaje = Personajes.query.get(id)

    personaje_selec = personaje.serialize()
    return jsonify(personaje_selec), 200

@app.route('/planetas/<int:id>', methods=['GET'])
def get_planeta(id):
    planeta = Planetas.query.get(id)

    planeta_selec = planeta.serialize()
    return jsonify(planeta_selec), 200

@app.route('/usuarios', methods=['POST'])
def post_usuario():
    request_usuario = request.get_json()

    user1 = Usuario(name=request_usuario["name"])
    db.session.add(user1)
    db.session.commit()
    return jsonify("all good"), 200

@app.route('/favoritos/<int:id>', methods=['DELETE'])
def delete_favorito(id):
    user1 = Favoritos.query.get(id)
    if user1 is None:
        raise APIException('User not found', status_code=404)

    db.session.delete(user1)
    db.session.commit()

    return jsonify("all good"), 200

@app.route('/usuarios/<int:id>/favoritos', methods=['GET'])
def get_usu(id):
    favoritos=Favoritos.query.filter_by(usuario_id=id)
    all_favoritos = list(map(lambda x: x.serialize(),favoritos))
    return jsonify(all_favoritos), 200

@app.route('/favoritos', methods=['GET'])
def get_favoritos():
    favoritos_query = Favoritos.query.all()
    all_favoritos = list(map(lambda x: x.serialize(), favoritos_query))
    return jsonify(all_favoritos), 200

@app.route('/favoritos/<int:id>', methods=['POST'])
def post_favoritos(id):
    request_favoritos = request.get_json()

    fav = Favoritos(personaje_name=request_favoritos["personaje_name"],planeta_name=request_favoritos["planeta_name"],usuario_id=id)
    db.session.add(fav)
    db.session.commit()
    return jsonify("all good"), 200

    

"""@app.route('/favorito/<int:id>', methods=['GET'])
def usuario_favorito(id):
    fav = Usuario.query.get(id)
    if fav is None:
        raise APIException('User not found', status_code=404)

    fav_selec = fav.serialize()

    return jsonify("all good"), 200"""

"""@app.route('/favoritos', methods=['GET'])
def get_planetas():
    favoritos_query = Favoritos.query.all()
    all_favoritos = list(map(lambda x: x.serialize(), favoritos_query))
    return jsonify(all_favoritos), 200"""

"""@app.route('/register', methods=["POST"])
def register():
    if request.method == 'POST':
        email = request.json.get("email", None)
        password = request.json.get("password", None)

        if not email:
            return jsonify({"msg": "email is required"}), 400
        if not password:
            return jsonify({"msg": "Password is required"}), 400

        user = User.query.filter_by(email=email).first()
        if user:
            return jsonify({"msg": "Username  already exists"}), 400
#crea un usuario nuevo
        user = Usuario()
        user.email = email
        hashed_password = generate_password_hash(password)
        print(password, hashed_password)

        user.password = hashed_password

        db.session.add(user)
        db.session.commit()

        return jsonify({"success": "Thanks. your register was successfully", "status": "true"}), 200"""



# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
