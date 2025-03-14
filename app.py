from flask import Flask, request, render_template
import requests
from deep_translator import GoogleTranslator  #Usado IA na tradução

app = Flask(__name__)

API_ENDPOINT = 'https://api.adviceslip.com/advice'

@app.route('/', methods=['GET', 'POST'])
def index():
    conselho = None  
    error = None

    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()

        if not nome:
            error = 'Nome é obrigatório'
        else:
            response = requests.get(API_ENDPOINT)

            if response.status_code == 200:
                dados = response.json()
                conselho = dados['slip']['advice']

                # Tradução do inglês- usado IA
                conselho = GoogleTranslator(source='auto', target='pt').translate(conselho)
            else:
                error = 'Erro ao buscar conselho. Tente novamente!'

    return render_template('index.html', nome=nome if 'nome' in locals() else None, conselho=conselho, error=error)

if __name__ == '__main__':
    app.run(debug=True, port=5002)

