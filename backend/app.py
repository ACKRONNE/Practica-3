from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db:5432/postgres'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    emails = db.Column(db.String(120), nullable=False)

    def json(self):
        return {'id': self.id, 'name': self.username, 'emails': self.emails}


with app.app_context():
    db.create_all()

#prueba
@app.route('/api/prueba', methods=['GET']) 
def prueba():
    return jsonify({'message': 'Hello World!'}),200 
