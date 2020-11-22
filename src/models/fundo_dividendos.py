from app import db
 
class FundoDividendos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fundo_id = db.Column(db.Integer, db.ForeignKey('fundo.id'))
    rendimento = db.Column(db.Numeric)
    data_base = db.Column(db.Date())
    data_pagamento = db.Column(db.Date())
    data_insercao = db.Column(db.DateTime(), default=db.func.now())

    fundo = db.relationship('Fundo')

    def __init__(self, fundo, rendimento, data_base, data_pagamento):
        self.fundo = fundo
        self.rendimento = rendimento
        self.data_base = data_base
        self.data_pagamento = data_pagamento