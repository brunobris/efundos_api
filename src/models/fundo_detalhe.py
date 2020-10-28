from app import db
 
class FundoDetalhe(db.Model):
    id = db.Column(db.Integer, db.ForeignKey("fundo.id"), primary_key=True)
    liquidez_diaria = db.Column(db.Integer)
    ultimo_rendimento = db.Column(db.Numeric)
    dividend_yield = db.Column(db.Numeric)
    patrimonio_liquido = db.Column(db.Numeric)
    valor_patrimonial = db.Column(db.Numeric)
    rentabilidade_mes = db.Column(db.Numeric)
    parent = db.relationship('Fundo', backref='fundo_detalhe')

    def __init__(self, parent):
        self.parent = parent