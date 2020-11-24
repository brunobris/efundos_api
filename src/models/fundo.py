from app import db
 
class Fundo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String())
    acronimo = db.Column(db.String())
    razao_social = db.Column(db.String())
    cnpj = db.Column(db.String())
    administrador = db.Column(db.String())
    inativo = db.Column(db.Boolean, default=False)
    data_insercao = db.Column(db.DateTime(), default=db.func.now())
    data_atualizacao = db.Column(db.Date())


    def __init__(self, codigo, acronimo, razao_social, administrador, cnpj):
        self.codigo = codigo
        self.acronimo = acronimo
        self.razao_social = razao_social
        self.administrador = administrador
        self.cnpj = cnpj

    def marcar_data_atualizacao(self):
        self.data_atualizacao = db.func.now()