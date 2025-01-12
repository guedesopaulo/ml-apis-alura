from flask import Flask
from textblob import TextBlob
from googletrans import Translator

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


app.run(debug=True)