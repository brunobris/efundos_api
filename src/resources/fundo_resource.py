import io
import logging
from flask import json, request, jsonify
from commons.util import json_success, json_with_status, validar_cpf
from app import db, app
from models.fundo import Fundo
from models.fundo_detalhe import FundoDetalhe
from flask_cors import CORS
import os

#Permite CORS em todas as rotas
CORS(app)

logger = logging.getLogger(__name__)

URL_RESOURCE_ARQUVO = '/fundos'
SISTEMA_ORIGEM = 2

@app.route(URL_RESOURCE_ARQUVO + '/atualizar-lista-fundos', methods=['POST'])
def update_lista_fundos():
  try:

    lista_fundos = request.json

    codigo = lista_fundos['codigo']
    nome = lista_fundos['nome']
    admin = lista_fundos['admin']
    
    fundo = Fundo(codigo, nome, admin) 
    db.session.add(fundo)

    fundoDetalhe = FundoDetalhe(
                    fundo, 3000, 50, 10.03)

    db.session.add(fundoDetalhe)
    

    db.session.commit() 
    
    return json_success(request.json, 'Fundo cadastrado.')
  except Exception as e:
    db.session.rollback()
    logger.exception('Erro ao cadastrar fundo.')
    return json_with_status(str(e), 500)