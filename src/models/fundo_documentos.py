from app import db
 
class FundoDocumentos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fundo_id = db.Column(db.Integer, db.ForeignKey('fundo.id'))
    nome = db.Column(db.String())
    link = db.Column(db.String())
    data_insercao = db.Column(db.DateTime(), default=db.func.now())

    fundo = db.relationship('Fundo')

    def __init__(self, fundo, nome, link):
        self.fundo = fundo
        self.nome = nome
        self.link = link