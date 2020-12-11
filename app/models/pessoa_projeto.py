from app import db


class PessoaProjeto(db.Model):
    __tablename__ = 'pessoa_projeto'
    id = db.Column(db.Integer, primary_key=True, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    users = db.relationship('User', back_populates='pessoa_projeto')

    project_id = db.Column(db.Integer, db.ForeignKey('projetos.id'), nullable=False)
    projetos = db.relationship('Projeto', back_populates='pessoa_projeto')

    type = db.Column(db.Integer, nullable=False)

    def __init__(self, user_id, project_id, type):
        self.user_id = user_id
        self.project_id = project_id
        self.type = type

