from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@host.docker.internal:5432/postgres'
db = SQLAlchemy(app)


# Modelo
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    emails = db.Column(db.String(120), nullable=False)

    def json(self):
        return {'id': self.id, 'name': self.username, 'emails': self.emails}

with app.app_context():
    db.create_all()

# Responde simplemente pong
@app.route('/GET/status/', methods=['GET'])
def status():
    return jsonify({'message': 'pong'}), 200

# Obtener una lista de todos los usuarios
@app.route('/GET/directories/', methods=['GET'])
def list_users():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        offset = (page - 1) * per_page

        users = User.query.offset(offset).limit(per_page).all()
        total_users = User.query.count()

        pagination = {
            'count': total_users,
            'next': None,
            'previous': None,
            'results': [user.json() for user in users]
        }

        if page > 1:
            pagination['previous'] = f'/directories/?page={page - 1}&per_page={per_page}'
        if page < total_users // per_page:
            pagination['next'] = f'/directories/?page={page + 1}&per_page={per_page}'

        # Intenta devolver la respuesta JSON
        response = jsonify(pagination)
        return response, 200
    except Exception as e:
        # Si ocurre un error, devuelve un mensaje de error y un código de estado 500
        error_response = jsonify({'error': 'Internal Server Error', 'message': str(e)}), 500
        return error_response

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

# Actualiza parcialmente un usuario.
@app.route('/PATCH/directories/<id>', methods=['PATCH'])
def update_user_patch(id):
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
