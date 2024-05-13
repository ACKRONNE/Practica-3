from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db:5432/postgres'
db = SQLAlchemy(app)


# Modelo de la base de datos
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    emails = db.Column(db.String(120), nullable=False)

    def json(self):
        return {'id': self.id, 'name': self.username, 'emails': self.emails}

# inicializa la bd
with app.app_context():
    db.create_all()

#  GET /status/ -> Responde simplemente pong en formato JSON
@app.route('/status/', methods=['GET'])
def status():
    return jsonify({'message': 'pong'}), 200

# GET /directories/{id} -> Obtener un usuario por id
@app.route('/GET/<id>', methods=['GET'])
def get_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            return jsonify(user.json()), 200
        else:
            return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        return jsonify({'message': 'error getting user','error':str(e)}), 500

# PATCH /directories/{id} -> Actualizar parcialmente un objeto.
@app.route('/PATCH/<id>', methods=['PATCH'])
def update_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            data = request.get_json()
            user.username = data.get('name', user.username)  
            user.emails = data.get('emails', user.emails)  
            db.session.commit()
            return jsonify(user.json()), 200
        else:
            return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        return jsonify({'message': 'error updating user','error':str(e)}), 500


# ----------------------------------------------------------------------------------------------------------------------------

# Creacion de usuarios
@app.route('/POST/directories/', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        new_user = User(username=data['name'], emails=data['emails'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'id': new_user.id,
                        'name': new_user.username,
                        'emails': new_user.emails}), 201
    except Exception as e:
        return jsonify({'message': 'error creating user','error':str(e)}), 500            


# Mostrar usuario por id
@app.route('/GET/directories/<id>', methods=['GET'])
def get_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            return jsonify(user.json()), 200
        else:
            return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        return jsonify({'message': 'error getting user','error':str(e)}), 500

# Actualizar usuario por id
@app.route('/PUT/directories/<id>', methods=['PUT'])
def update_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            data = request.get_json()
            user.username = data['name']
            user.emails = data['emails']
            db.session.commit()
            return jsonify(user.json()), 200
        else:
            return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        return jsonify({'message': 'error updating user','error':str(e)}), 500

# Delete de usuarios por id
@app.route('/DELETE/directories/<id>', methods=['DELETE'])
def delete_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify({'message': 'User deleted'}), 200
        else:
            return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        return jsonify({'message': 'error deleting user','error':str(e)}), 500


@app.route('/api/prueba', methods=['GET']) 
def prueba():
    return jsonify({'message': 'Hello World!'}),200 
