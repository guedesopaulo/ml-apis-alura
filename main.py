import pandas as pd
import pickle

from flask import Flask
from flask import jsonify
from flask_basicauth import BasicAuth
from flask import request
from googletrans import Translator
from textblob import TextBlob

model = pickle.load(open('modelo.sav', 'rb'))
colunas = ['tamanho', 'ano', 'garagem']


app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = 'paulo'
app.config['BASIC_AUTH_PASSWORD'] = 'alura'

basic_auth = BasicAuth(app)

@app.route('/')
def home():
    return "Minha Primeira API."

@app.route('/sentimento/<frase>')
@basic_auth.required
def sentimento(frase):
    translator = Translator()
    traducao = translator.translate(frase, src='pt', dest='en')
    tb = TextBlob(traducao.text)
    polatidade = tb.sentiment.polarity
    return f"polatidade {polatidade}"


@app.route('/cotacao/', methods = ['POST'])
@basic_auth.required
def cotacao():
    dados = request.get_json()
    dados_input = [dados[col] for col in colunas]
    preco = model.predict([dados_input])
    return jsonify(preco=preco[0])

app.run(debug=True)