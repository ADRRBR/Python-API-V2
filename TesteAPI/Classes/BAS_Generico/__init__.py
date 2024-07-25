import sys

import warnings
warnings.simplefilter(action='ignore', category=UserWarning)

import pyodbc
import pandas as pd
from enum import Enum

from datetime import datetime as dtm

from flask import Flask, make_response, jsonify, request
import json
import numpy
import requests

# Tipos de Retorno para Execução dos Métodos da Classes
class StatusExecucao(Enum):
    SemRequisicao = 0
    Encontrado = 1
    NaoEncontrado = 2
    Sucesso = 3
    Erro = 4
    Confirmado = 5
    Cancelado = 6

# Converter objetos de coleção contendo tipos de dados não serializáveis não serializáveis em JSON
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.integer):
            return int(obj)
        if isinstance(obj, numpy.floating):
            return float(obj)
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)

class DigitacaoValores(Enum):
    Cancelado = -999999
    Invalido = -444444

def DigMoeda(Mensagem):
    try:
        valor = float(input(Mensagem))
    except (ValueError, TypeError) as erro:
        valor = DigitacaoValores.Invalido
    except KeyboardInterrupt as erro:
        valor = DigitacaoValores.Cancelado

    return valor

def DigNumero(Mensagem):
    try:
        valor = int(input(Mensagem))
    except (ValueError, TypeError) as erro:
        valor = DigitacaoValores.Invalido
    except KeyboardInterrupt as erro:
        valor = DigitacaoValores.Cancelado

    return valor