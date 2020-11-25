import logging  
from app import db, app
from flask import json, jsonify, request
from flask_jwt_extended import (
    jwt_required, create_access_token
)
import datetime

logger = logging.getLogger(__name__)



URL_RESOURCE_ARQUVO = '/security'

# @jwt.user_claims_loader
# def add_claims_to_access_token(identity):
#     return {
#         'roles': ['admin']
#     }


@app.route(URL_RESOURCE_ARQUVO + '/login', methods=['POST'])
def login():
    access_token = create_access_token(identity='1')
    return jsonify(access_token=access_token), 200


@app.route(URL_RESOURCE_ARQUVO + '/create-api-token', methods=['POST'])
def create_api_token():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if username != 'efundos-scraper' or password != "eFuNdOs!2020#":
        return jsonify({"msg": "Usuário ou senha inválidos"}), 401

    expires = datetime.timedelta(hours=22)
    token = create_access_token(identity=username, expires_delta=expires, fresh=True)
    return jsonify({'token': token}), 201