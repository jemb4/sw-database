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
from models import db, User, Planets, Characters, Favorites
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


# USERS ----------

@app.route('/user', methods=['GET', 'POST'])
def user():
    if request.method == 'GET':
        user = User.query.all()
        all_users = list(map(lambda user: user.serialize(), user))
        return jsonify(all_users), 201
    
    if request.method == 'POST':
        body = request.get_json()
        user = User(name=body['name'], email=body['email'], password=body['password'])
        db.session.add(user)
        db.session.commit()
        return jsonify(user.serialize()), 201

# CHARACTER ---------------

@app.route('/character', methods=['GET', 'POST'])
def characters():
    if request.method == 'GET':
        character = Characters.query.all()
        all_character = list(map(lambda character: character.serialize(), character))
        return jsonify(all_character), 201
    
    if request.method == 'POST':
        body = request.get_json()
        character = Characters(id=body['id'], name=body['name'])
        db.session.add(character)
        db.session.commit()
        return jsonify(character.serialize()), 201

@app.route('/character/<int:character_id>', methods=['GET', 'PUT', 'DELETE'])
def determinate_character(character_id):
    if request.method == 'GET':
        character = Characters.query.get(character_id)
        if people is None:
            raise APIException("This character doesn't exist", 404)

        return jsonify(character.serialize())
    
    if request.method == 'PUT':
        character = Characters.query.get(character_id)
        if character is None:
            raise APIException("This character doesn't exist", 404)
        body = request.get_json()

        if not ("id" in body):
            raise APIException("id not exist", 404)

        character.name = body["name"]
        character.eyes = body["eye_color"]
        character.birth = body["birth_year"]
        db.session.commit()

        return jsonify(people.serialize())

    if request.method == 'DELETE':
        character = Characters.query.get(character_id)
        if people is None:
            raise APIException("This character doesn't exist", 404)
            db.session.delete(character)
            deb.session.commit()

            return jsonify(people.serialize())

# PLANETS ----------

@app.route('/planets', methods=['GET', 'POST'])
def planets():
    if request.method == 'GET':
        planets = Planets.query.all()
        all_planets = list(map(lambda planets: planets.serialize(), planets))
        return jsonify(all_planets), 201
    
    if request.method == 'POST':
        body = request.get_json()
        planets = Planets(id=body['id'], name=body['name'])
        db.session.add(planets)
        db.session.commit()
        return jsonify(planets.serialize()), 201

@app.route('/character/<int:planets_id>', methods=['GET', 'PUT', 'DELETE'])
def determinate_planets(planets_id):
    if request.method == 'GET':
        planets = planetss.query.get(planets_id)
        if people is None:
            raise APIException("This planets doesn't exist", 404)

        return jsonify(planets.serialize())
    
    if request.method == 'PUT':
        planets = Planets.query.get(planets_id)
        if planets is None:
            raise APIException("This planets doesn't exist", 404)
        body = request.get_json()

        if not ("id" in body):
            raise APIException("id not exist", 404)

        planets.name = body["name"]
        planets.population = body["population"]
        planets.terrain = body["terrain"]
        db.session.commit()

        return jsonify(people.serialize())

    if request.method == 'DELETE':
        planets = Planets.query.get(planets_id)
        if people is None:
            raise APIException("This planets doesn't exist", 404)
            db.session.delete(planets)
            deb.session.commit()

            return jsonify(people.serialize())

# FAVORITES ------->

@app.route('/user/<int:user_id>/favorites', methods=['GET'])
def get_all_favs(user_id):
    favs = Favorites.query.filter_by(user_id=user_id)
    all_favorites = list(map(lambda favorites: favorites.seralize(), favorites))
    return jsonify(all_favorites)

@app.route('/user/<int:user_id>/favorites/<int:favorite_id>', methods=['GET'])
def post_fav(user_id, character_id, planets_id):
    if character_id is None AND planets_id is not None:
        favplanet = Favorites(user_id=user_id, planet_id=planet_id)
        db.session.add(favplanet)
        db.session.commit()

        return jsonify(favorites.serialize()), 201
    
    if character_id is not None AND planets_id is None:
        favchar = Favorites(user_id=user_id, character_id=character_id)
        db.session.add(favcharacter)
        db.session.commit()

        return jsonify(favorites.serialize()), 201

@app.route('/user/')

    
# this only runs if `$ python src/main.py` is executed

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
