import io
import logging
from flask import json, request, jsonify, Response
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

@app.route(URL_RESOURCE_ARQUVO + '/atualizar-fundo', methods=['POST'])
def update_lista_fundos():
  try:
    fundo_request = request.get_json()

    codigo = fundo_request['symbol']
    nome = fundo_request['nome']
    admin = fundo_request['admin']

    detalhe_request = fundo_request['detalhe']
    
    #TODO: Verificar se Fundo já existe, se não existir cadastra

    fundo = Fundo(codigo, nome, admin)
    db.session.add(fundo)

    #TODO: Buscar detalhes do fundo, e setar os dados novamente (para não ficar procurando o que mudou)
    
    if detalhe_request:
      fundoDetalhe = FundoDetalhe(
                        parent = fundo, 
                        liquidez_diaria = detalhe_request['liquidez_diaria'], 
                        ultimo_rendimento = detalhe_request['ultimo_rendimento'],
                        dividend_yield = detalhe_request['dy'],
                        patrimonio_liquido = detalhe_request['patrimonio_liquido'],
                        valor_patrimonial = detalhe_request['valor_patrimonial'],
                        rentabilidade_mes = detalhe_request['rentabilidade_mes']
                      )

      db.session.add(fundoDetalhe)

    db.session.commit() 
    
    return json_success(request.json, 'Fundo cadastrado.')
  except Exception as e:
    #db.session.rollback()
    logger.warning(e)
    logger.exception('Erro ao cadastrar fundo.', exc_info=False)
    return Response('', status=500)
    # return json_with_status(str(e), 500)