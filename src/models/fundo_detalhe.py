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

    def __init__(
        self, 
        parent, 
        liquidez_diaria=None, 
        ultimo_rendimento=None, 
        dividend_yield=None, 
        patrimonio_liquido=None, 
        valor_patrimonial=None, 
        rentabilidade_mes=None):

        self.parent = parent
        self.liquidez_diaria = liquidez_diaria
        self.ultimo_rendimento = ultimo_rendimento
        self.dividend_yield = dividend_yield
        self.patrimonio_liquido = patrimonio_liquido
        self.valor_patrimonial = valor_patrimonial
        self.rentabilidade_mes = rentabilidade_mes
