from app import db
 
class Fundo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String())
    nome = db.Column(db.String())
    cnpj = db.Column(db.String())
    administrador = db.Column(db.String())
    data_insercao = db.Column(db.DateTime(), default=db.func.now())
    data_atualizacao = db.Column(db.Date())

    def __init__(self, codigo, nome, administrador):
        self.codigo = codigo
        self.nome = nome
        self.administrador = administrador

    def marcar_data_atualizacao(self):
        self.data_atualizacao = db.func.now()