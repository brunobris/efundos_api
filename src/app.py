from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
    
app = Flask(__name__)

#Configurações do SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Seta o limite máximo de upload para 8 MB
#Esta configuração terá efeito sobre TODOS os requests
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024

db = SQLAlchemy(app)