from flask import Flask

app = Flask(__name__)

@app.route('/api/hello', methods=['GET'])
def hello_world():
    return "Olá, Seja Bem Vindo", 200

@app.route('/', methods=['GET'])
def hello_world():
    return "Página Principal", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
