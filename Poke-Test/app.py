from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import requests
import os



app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pokemon.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    image_url = db.Column(db.String(200))
    types = db.Column(db.String(200))
    height = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    abilities = db.Column(db.String(200)) 
    
    
    def to_dict(self, detail=False):
        base = {'name': self.name, 'image': self.image_url}
        if detail:
            base.update({
                'types': self.types.split(',') if self.types else [],
                'height': self.height,
                'weight': self.weight,
                'abilities': self.abilities.split(',') if self.abilities else []
            })
        return base
    
with app.app_context():
    db.create_all()

POKEAPI_URL = "https://pokeapi.co/api/v2/pokemon"

def fetch_and_store_pokemon_data(name):
    existing_pokemon = Pokemon.query.filter_by(name=name).first()
    if existing_pokemon:
        return existing_pokemon
    response = requests.get(f"{POKEAPI_URL}/{name}")
    if response.status_code != 200:
        return None
    data = response.json()
    types = ','.join([t['type']['name'] for t in data.get('types', [])])
    abilities = ','.join([a['ability']['name'] for a in data.get('abilities', [])])
    image_url = data.get('sprites', {}).get('front_default')
    pokemon = Pokemon(
        name=name,
        image_url=image_url,
        types=types,
        height=data.get('height'),
        weight=data.get('weight'),
        abilities=abilities
    )
    db.session.add(pokemon)
    db.session.commit()
    return pokemon

@app.route('/api/pokemon', methods=['GET'])
def get_pokemon_list():
    limit = 20
    db_count = Pokemon.query.count()
    if db_count < limit:
        response = requests.get(f"{POKEAPI_URL}?limit={limit}")
        if response.status_code != 200:
            return jsonify({'error': 'Failed to fetch from Pokemon API'}), 500
        data = response.json()
        for item in data.get('results', []):
            fetch_and_store_pokemon_data(item['name'])
    pokemons = Pokemon.query.limit(limit).all()
    return jsonify([p.to_dict() for p in pokemons])

@app.route('/api/pokemon/<string:name>', methods=['GET'])
def get_pokemon_detail(name):
    pokemon = Pokemon.query.filter_by(name=name).first()
    if not pokemon:
        pokemon = fetch_and_store_pokemon_data(name)
        if not pokemon:
            return jsonify({'error': 'Pokemon not found'}), 404
    return jsonify(pokemon.to_dict(detail=True))

@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(debug=True)