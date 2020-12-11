from app import db


class Notificacao(db.Model):
    __tablename__ = 'notificacoes'
    id = db.Column(db.Integer, primary_key=True, nullable=False)

    date = db.Column(db.DateTime, nullable=False)
    type = db.Column(db.Integer, nullable=False)

    was_accepted = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    users = db.relationship('User', back_populates='notificacoes')

    project_id = db.Column(db.Integer, db.ForeignKey('projetos.id'), nullable=False)
    projetos = db.relationship('Projeto', back_populates='notificacoes')

    def __init__(self, date, type, was_accepted, user_id, project_id):
        self.date = date
        self.type = type
        self.was_accepted = was_accepted
        self.user_id = user_id
        self.project_id = project_id


