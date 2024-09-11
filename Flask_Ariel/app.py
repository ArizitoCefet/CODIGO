# verifico a pasta do meu projeto, verifico se está no meu github
# git remote -v
# e executo
# git pull origin master
# quero clonar o projeto
# git clone https://...
# instalo a extensao python
# abro o terminal e verifico se abre no venv, caso não abra, eu devo executar
# ctrl shift p
# e digitar envrironment e pedir para criar um ambiente virtual
# pip install flask
# pip install Flask-SQLAlchemy
# pip install Flask-Migrate
# pip install Flask-Script
# pip install pymysql
# flask db init
# flask db migrate -m "Migração Inicial"
# flask db upgrade
# flask run --debug

from flask import Flask, render_template, request, flash, redirect
app = Flask(__name__)
from database import db
from flask_migrate import Migrate
from models import Funcionario
app.config['SECRET_KEY'] = 'cd6ec8a03ee6252de83e921bd4be5e016819ed51221599fea40e5cbfd110ecce'

# drive://usuario:senha@servidor/banco_de_dados
conexao = "mysql+pymysql://alunos:cefetmg@127.0.0.1/flaskG2"
app.config['SQLALCHEMY_DATABASE_URI'] = conexao
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dados', methods=['POST'])
def dados():
    flash('Dados enviados!!')
    dados = request.form
    return render_template('dados.html', dados=dados)

@app.route('/funcionario')
def funcionario():
    u = Funcionario.query.all()
    return render_template('funcionario_lista.html', dados = u)

@app.route('/funcionario/add')
def funcionario_add():
    return render_template('funcionario_add.html')

@app.route('/funcionario/save', methods=['POST'])
def funcionario_save():
    nome = request.form.get('nome')
    cargo = request.form.get('cargo')
    data_admissao = request.form.get('data_admissao')
    if nome and cargo and data_admissao:
        funcionario = Funcionario(nome, cargo, data_admissao)
        db.session.add(funcionario)
        db.session.commit()
        flash('Funcionário cadastrado com sucesso!!!')
        return redirect('/funcionario')
    else:
        flash('Preencha todos os campos!!!')
        return redirect('/funcionario/add')

@app.route('/funcionario/remove/<int:id_produto>')
def funcionario_remove(id_produto):
    funcionario = Funcionario.query.get(id_produto)
    if funcionario:
        db.session.delete(funcionario)
        db.session.commit()
        flash('Funcionário removido com sucesso!!!')
        return redirect('/funcionario')
    else:
        flash('Caminho incorreto!!!')
        return redirect('/funcionario')
    
@app.route('/funcionario/edita/<int:id_produto>')
def funcionario_edita(id_produto):
    funcionario = Funcionario.query.get(id_produto)
    return render_template('funcionario_edita.html', dados = funcionario)

@app.route('/funcionario/editasave', methods=['POST'])
def funcionario_editasave():
    nome = request.form.get('nome')
    cargo = request.form.get('cargo')
    data_admissao = request.form.get('data_admissao')
    id_produto = request.form.get('id_produto')
    if id_produto and nome and cargo and data_admissao:
        funcionario = Funcionario.query.get(id_produto)
        funcionario.nome = nome
        funcionario.cargo = cargo
        funcionario.data_admissao = data_admissao
        db.session.commit()
        flash('Dados atualizados com sucesso!!!')
        return redirect('/funcionario')
    else:
        flash('Faltando dados!!!')
        return redirect('/funcionario')


if __name__ == '__main__':
    app.run()
