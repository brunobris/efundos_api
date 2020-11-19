from app import db
 
class FundoDocumentos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fundo_id = db.Column(db.Integer, db.ForeignKey('fundo.id'))
    fnet_id = db.Column(db.Integer)
    nome = db.Column(db.String())
    data_publicacao = db.Column(db.DateTime())
    data_referencia = db.Column(db.DateTime())
    data_insercao = db.Column(db.DateTime(), default=db.func.now())

    fundo = db.relationship('Fundo')

    def __init__(self, fundo, nome, fnet_id, data_publicacao, data_referencia):
        self.fundo = fundo
        self.nome = nome
        self.fnet_id = fnet_id
        self.data_publicacao = data_publicacao
        self.data_referencia = data_referencia