import io
import logging
from flask import json, request, jsonify, Response
from commons.util import json_success, json_with_status, validar_cpf
from app import db, app
from models.fundo import Fundo
from models.fundo_detalhe import FundoDetalhe
from models.fundo_documentos import FundoDocumentos
from models.fundo_dividendos import FundoDividendos
from flask_cors import CORS
from flask_jwt_extended import jwt_required
from security.roles_decorators import scraper_only

import os

#Permite CORS em todas as rotas
CORS(app)

logger = logging.getLogger(__name__)

URL_RESOURCE_ARQUVO = '/fundos'

#Retirar esta rota, é apenas para testes
@app.route(URL_RESOURCE_ARQUVO + '/teste', methods=['GET'])
@scraper_only
def teste():
  return jsonify([]), 200



@app.route(URL_RESOURCE_ARQUVO + '/atualizar-fundo', methods=['POST'])
def update_lista_fundos():
  try:
    fundo_request = request.get_json()

    codigo = fundo_request['symbol']
    acronimo = fundo_request['symbol']
    razao_social = fundo_request['razao_social']
    admin = fundo_request['admin']
    cnpj = fundo_request['cnpj']
    detalhe_request = fundo_request['detalhe']
    lista_documentos = fundo_request['detalhe']['lista_documentos']
    lista_dividendos = fundo_request['detalhe']['lista_dividendos']

    fundo = db.session.query(Fundo).filter(Fundo.codigo.ilike(codigo)).first()

    fundo_detalhe = None
    if fundo is None:
      fundo = Fundo(codigo.upper(), acronimo.upper(), razao_social, admin, cnpj)
      db.session.add(fundo)

    #Marca fundo como atualizado com a data do banco de dados
    fundo.marcar_data_atualizacao()

    fundo_detalhe = db.session.query(FundoDetalhe).get(fundo.id) if fundo.id else None
    if fundo_detalhe == None:
      fundo_detalhe = FundoDetalhe(parent = fundo)

    fundo_detalhe.liquidez_diaria = detalhe_request['liquidez_diaria'] 
    fundo_detalhe.ultimo_rendimento = detalhe_request['ultimo_rendimento']
    fundo_detalhe.dividend_yield = detalhe_request['dy']
    fundo_detalhe.patrimonio_liquido = detalhe_request['patrimonio_liquido']
    fundo_detalhe.rentabilidade_mes = detalhe_request['rentabilidade_mes']
                      
    db.session.add(fundo_detalhe)
    atualiza_documentos(fundo, lista_documentos)
    atualiza_dividendos(fundo, lista_dividendos)

    db.session.commit() 
    
    return json_success(request.json, 'Fundo cadastrado.')
  except Exception as e:
    db.session.rollback()
    logger.warning(e)
    logger.exception('Erro ao cadastrar fundo.')
    return json_with_status(str(e), 500)

def atualiza_documentos(fundo, lista_documentos):

  #Retorna lista de documentos, caso já existam
  #TODO: Talvez aqui seria interessante trazer apenas os últimas 20 registros ordenados por data publicação
  documentos_existentes = db.session.query(FundoDocumentos).filter(FundoDocumentos.fundo_id == fundo.id).all() if fundo.id else []
  
  #Compara as duas lista, e adiciona apenas os documentos não cadastrados
  lista_links_existentes = list(map(lambda doc : doc.fnet_id, documentos_existentes))

  lista_docs_para_adicionar = [doc for doc in lista_documentos if int(doc['fnet_id']) not in lista_links_existentes]

  for doc in lista_docs_para_adicionar:
    fundo_documento = FundoDocumentos(fundo, doc['nome'], doc['fnet_id'], doc['data_publicacao'], doc['data_referencia'])
    db.session.add(fundo_documento)

def atualiza_dividendos(fundo, lista_dividendos):
  #logger.warning(lista_dividendos)

  #TODO: Talvez aqui seria interessante trazer apenas os últimas 20 registros ordenados por data publicação
  dividendos_cadastrados = db.session.query(FundoDividendos).filter(FundoDividendos.fundo_id == fundo.id).all() if fundo.id else []
  
  lista_dividendos_cadastrados = list(map(lambda div : str(div.data_base), dividendos_cadastrados))

  logger.warning("Div cadastrados: ")
  logger.warning(lista_dividendos_cadastrados)

  logger.warning("Div request:")
  logger.warning(lista_dividendos)

  #TODO: Melhorar a comparação, talvez seja melhor o scrapper já enviar a data sem horario
  dividendos_para_cadastrar = [div for div in lista_dividendos if div['data_base'][:10] not in lista_dividendos_cadastrados]

  logger.warning("Div para cadastrar: ")
  logger.warning(dividendos_para_cadastrar)
  for dividendo in dividendos_para_cadastrar:
    fundo_dividendos = FundoDividendos(fundo, dividendo['rendimento'],
                        dividendo['data_base'], dividendo['data_pagamento'] )
    db.session.add(fundo_dividendos)