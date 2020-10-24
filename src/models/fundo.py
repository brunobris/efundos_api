from app import db
 
class Fundo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String())
    nome = db.Column(db.String())
    administrador = db.Column(db.String())
    data_inicio = db.Column(db.DateTime(), default=db.func.now())

    def __init__(self, codigo, nome, administrador):
        self.codigo = codigo
        self.nome = nome
        self.administrador = administrador