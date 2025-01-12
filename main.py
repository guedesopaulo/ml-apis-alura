import pandas as pd

from flask import Flask
from flask import jsonify
from flask import request
from googletrans import Translator
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from textblob import TextBlob


df = pd.read_csv("casas.csv")

colunas = ['tamanho', 'ano', 'garagem']

X = df.drop('preco', axis=1)
y = df['preco']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
model= LinearRegression()
model.fit(X_train, y_train)

app = Flask(__name__)

@app.route('/')
def home():
    return "Minha Primeira API."

@app.route('/sentimento/<frase>')
def sentimento(frase):
    translator = Translator()
    traducao = translator.translate(frase, src='pt', dest='en')
    tb = TextBlob(traducao.text)
    polatidade = tb.sentiment.polarity
    return f"polatidade {polatidade}"


@app.route('/cotacao/', methods = ['POST'])
def cotacao():
    dados = request.get_json()
    dados_input = [dados[col] for col in colunas]
    preco = model.predict([dados_input])
    return jsonify(preco=preco[0])

app.run(debug=True)