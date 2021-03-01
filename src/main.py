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


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
