from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)  # Cria uma instância da aplicação Flask.
app.config['SECRET_KEY'] = 'sua_chave_secreta'  # Define uma chave secreta para a sessão.
socketio = SocketIO(app)  # Inicializa o Flask-SocketIO com a aplicação Flask.

# Define uma rota para a URL raiz.
@app.route("/") #Ao entrar no site, a função ABAIXO DE "app.route("/")" é automaticamente executada, não é explicito, mas o Flask faz isso
def home():
    return render_template("index.html")  # Retorna o template HTML quando a rota é acessada.

@socketio.on('connect')  # Define um manipulador de evento para quando um cliente se conecta.
def handle_connect():
    print('Cliente conectado')  # Imprime uma mensagem no servidor.

@socketio.on('disconnect')  # Define um manipulador de evento para quando um cliente se desconecta.
def handle_disconnect():
    print('Cliente desconectado')  # Imprime uma mensagem no servidor.

@socketio.on('message')
def handle_message(data):
    # 'data' é um objeto que contém 'message' e 'name'
    print('Mensagem recebida:', data['message'])
    print('Nome:', data['name'])
    # Emite uma resposta para o cliente incluindo a mensagem e o nome
    socketio.emit('response', {'message': data['message'], 'name': data['name']})


if __name__ == '__main__':
    socketio.run(app, debug=True)  # Executa a aplicação se o script for o principal.
