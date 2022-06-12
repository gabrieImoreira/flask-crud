from flask import Flask, request, jsonify
from flask_pydantic_spec import FlaskPydanticSpec, Request, Response
from pydantic import BaseModel
from tinydb import TinyDB, Query
from typing import Optional
import math


### inicio 
server = Flask(__name__) # iniciando flask
spec = FlaskPydanticSpec('flask', title='Learning') #iniciando swagger
spec.register(server) 
db = TinyDB('database.json') #iniciando db

class Pessoa(BaseModel):
    id: Optional[int]
    nome: str
    idade: int 

class Pessoas(BaseModel):
    pessoas: list[Pessoa]
    count: int

@server.get('/pessoas')
@spec.validate(resp=Response(HTTP_200=Pessoas))
def buscar_pessoas():
    """Retornar todas as pessoas do db"""
    return jsonify(
        Pessoas(
            pessoas=db.all(),
            count=len(db.all())
        ).dict()
    )

@server.post('/pessoas')
@spec.validate(body=Request(Pessoa), resp=Response(HTTP_200=Pessoa))
def inserir_pessoas():
    """Insere uma pessoa no db"""
    body = request.context.body.dict()
    db.insert(body)
    return body

@server.put('/pessoas/<int:id>')
@spec.validate(
    body=Request(Pessoa), resp=Response(HTTP_200=Pessoa)
)
def altera_pessoa(id):
    """Altera pessoas no db com base no id"""
    Pessoa = Query()
    body = request.context.body.dict()
    db.update(body, Pessoa.id == id)
    return jsonify(body)


@server.delete('/pessoas/<int:id>')
@spec.validate(
    body=Request(Pessoa), resp=Response('HTTP_200')
)
def deleta_pessoa(id):
    """Deleta pessoas no db com base no id"""
    Pessoa = Query()
    db.remove(Pessoa.id == id)
    return jsonify({})

server.run()


#windows
#set FLASK_APP=main.py 
#$env:FLASK_APP = "main.py" 
#flask run
