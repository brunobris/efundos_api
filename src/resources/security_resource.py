import logging  
from app import db, app
from flask import json, jsonify
from flask_jwt_extended import (
    jwt_required, create_access_token,
    get_jwt_identity
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
    username = get_jwt_identity()
    expires = datetime.timedelta(hours=22)
    token = create_access_token(username, expires_delta=expires)
    return jsonify({'token': token}), 201