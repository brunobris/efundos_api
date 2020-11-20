import io
import logging
from flask import json, request, jsonify, Response
from commons.util import json_success, json_with_status, validar_cpf
from app import db, app
from models.fundo import Fundo
from models.fundo_detalhe import FundoDetalhe
from models.fundo_documentos import FundoDocumentos
from flask_cors import CORS
import os

#Retirar
# import time

#Permite CORS em todas as rotas
CORS(app)

logger = logging.getLogger(__name__)

URL_RESOURCE_ARQUVO = '/fundos'
SISTEMA_ORIGEM = 2

#Retirar esta rota, é apenas para testes
# @app.route(URL_RESOURCE_ARQUVO + '/teste-timeout', methods=['GET'])
# def teste_timeout():
#   time.sleep(2)
#   return Response(status=200)

@app.route(URL_RESOURCE_ARQUVO + '/atualizar-fundo', methods=['POST'])
def update_lista_fundos():
  try:
    fundo_request = request.get_json()

    codigo = fundo_request['symbol']
    nome = fundo_request['nome']
    admin = fundo_request['admin']
    detalhe_request = fundo_request['detalhe']
    lista_documentos = fundo_request['detalhe']['lista_documentos']
    
    fundo = db.session.query(Fundo).filter(Fundo.codigo.ilike(codigo)).first()

    fundo_detalhe = None
    if fundo is None:
      fundo = Fundo(codigo.upper(), nome, admin)
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

    db.session.commit() 
    
    return json_success(request.json, 'Fundo cadastrado.')
  except Exception as e:
    db.session.rollback()
    logger.warning(e)
    logger.exception('Erro ao cadastrar fundo.')
    return json_with_status(str(e), 500)

def atualiza_documentos(fundo, lista_documentos):

  #Retorna lista de documentos, caso já existam
  #TODO: Talvez aqui seria interessante trazer apenas os últimas 20 registros ordenados por daa publicação
  documentos_existentes = db.session.query(FundoDocumentos).filter(FundoDocumentos.fundo_id == fundo.id).all() if fundo.id else []
  
  #Compara as duas lista, e adiciona apenas os documentos não cadastrados
  lista_links_existentes = list(map(lambda doc : doc.fnet_id, documentos_existentes))

  lista_docs_para_adicionar = [doc for doc in lista_documentos if int(doc['fnet_id']) not in lista_links_existentes]

  for doc in lista_docs_para_adicionar:
    fundo_documento = FundoDocumentos(fundo, doc['nome'], doc['fnet_id'], doc['data_publicacao'], doc['data_referencia'])
    db.session.add(fundo_documento)