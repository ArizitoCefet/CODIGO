from database import db

class Funcionario(db.Model):
    __tablename__="funcionario"
    id_produto = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(100))
    cargo = db.Column(db.String(50))
    data_admissao = db.Column(db.Date)

    def __init__(self, nome, cargo, data_admissao):
        self.nome = nome
        self.cargo = cargo
        self.data_admissao = data_admissao

    def __repr__(self):
        return "<Funcionario {}>".format(self.nome)