from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import os
    
app = Flask(__name__)

#Configurações do SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Configurações do Flask-JWT-Extended
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!

jwt = JWTManager(app)

#Seta o limite máximo de upload para 8 MB
#Esta configuração terá efeito sobre TODOS os requests
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024

db = SQLAlchemy(app)