import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Função para verificar se o login é válido
def verificar_login(username, senha):
    with open('usuarios.json', 'r') as arquivo:
        usuarios = json.load(arquivo)
        for usuario in usuarios:
            if usuario['username'] == username and usuario['senha'] == senha:
                return True
    return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        novo_usuario = {
            'Perfil': request.form['Perfil'],
            'razao_social': request.form['razao_social'],
            'cnpj': request.form['cnpj'],
            'endereco': request.form['endereco'],
            'numero': request.form['numero'],
            'cidade': request.form['cidade'],
            'estado': request.form['estado'],
            'bairro': request.form['bairro'],
            'email': request.form['email'],
            'telefone': request.form['telefone'],
            'username': request.form['username'],
            'senha': request.form['senha']
        }
        with open('usuarios.json', 'r') as arquivo:
            usuarios = json.load(arquivo)
        usuarios.append(novo_usuario)
        with open('usuarios.json', 'w') as arquivo:
            json.dump(usuarios, arquivo)
        return redirect('/')
    return render_template('formulario_registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        senha = request.form['senha']

        if verificar_login(username, senha):
            with open('usuarios.json', 'r') as arquivo:
                registros = json.load(arquivo)
            return render_template('lista_registros.html', registros=registros, usuario_logado=username)
        else:
            return render_template('tela_login.html', erro="Nome de usuário ou senha incorretos.")
    return render_template('tela_login.html')

@app.route('/editar/<username>', methods=['GET', 'POST'])
def editar(username):
    if request.method == 'POST':
        with open('usuarios.json', 'r') as arquivo:
            usuarios = json.load(arquivo)
        
        for usuario in usuarios:
            if usuario['username'] == username:
                usuario['Perfil'] = request.form['Perfil']
                usuario['razao_social'] = request.form['razao_social']
                usuario['cnpj'] = request.form['cnpj']
                usuario['endereco'] = request.form['endereco']
                usuario['numero'] = request.form['numero']
                usuario['cidade'] = request.form['cidade']
                usuario['estado'] = request.form['estado']
                usuario['bairro'] = request.form['bairro']
                usuario['email'] = request.form['email']
                usuario['telefone'] = request.form['telefone']
                usuario['senha'] = request.form['senha']
                break

        with open('usuarios.json', 'w') as arquivo:
            json.dump(usuarios, arquivo)
        return redirect('/login')
    
    with open('usuarios.json', 'r') as arquivo:
        usuarios = json.load(arquivo)
    
    usuario_editar = None
    for usuario in usuarios:
        if usuario['username'] == username:
            usuario_editar = usuario
            break
    
    return render_template('editar_usuario.html', usuario=usuario_editar)

if __name__ == '__main__':
    app.run(debug=True)
