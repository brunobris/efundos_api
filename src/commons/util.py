"""
Common methods to use across the processes 
"""
from flask import Response, json
import re

def fill_entity(data, entity):
    """
        Metodo para setar os campos na entidade.

    Arguments:
        data {dict} -- data from request
        entity {Model} -- Model Object to persist

    Returns:
        Model -- Entity with the fields filled
    """
    for item in data.keys():
        if item in entity._table_.columns:
            entity._setattr_(item, data[item])

    return entity


def json_success(data: dict = None, message: str = ''):
    response_data = {
        "data": data,
        "message":message
    }
    return Response(json.dumps(response_data), status=200,mimetype='application/json')

def json_with_status(data: dict = None, status_code: int = 400, message: str = ''):
    response_data = {
        "data": data,
        "message":message
    }
    
    return Response(json.dumps(response_data), status=status_code,mimetype='application/json')

def validar_cpf(cpf):
    """
        Valida o CPF e dispara uma expcetion caso não esteja no formato esperado
       
    Arguments:
        cpf {string} -- cpf from request

    Returns:
    """
    if not re.match('^([\s\d]+)$', cpf):
        raise Exception('O cpf: {} é inválido'.format(cpf))

    # Podemos fixar tamanho 11 ?
    #if len(cpf) < 11:
        #raise Exception('O cpf: {} é inválido'.format(cpf))

    def calc(t): return int(t[1]) * (t[0] + 2)
    d1 = (sum(map(calc, enumerate(reversed(cpf[:-2])))) * 10) % 11
    d2 = (sum(map(calc, enumerate(reversed(cpf[:-1])))) * 10) % 11

    if str(d1) == cpf[-2] and str(d2) == cpf[-1]:
        return

    raise Exception('O cpf: {} é inválido'.format(cpf))