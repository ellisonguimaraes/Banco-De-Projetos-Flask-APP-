from app import db


class Notificacao(db.Model):
    __tablename__ = 'notificacoes'
    id = db.Column(db.Integer, primary_key=True, nullable=False)

    date = db.Column(db.Date, nullable=False)
    type = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    users = db.relationship('User', back_populates='notificacoes')

    project_id = db.Column(db.Integer, db.ForeignKey('projetos.id'), nullable=False)
    projetos = db.relationship('Projeto', back_populates='notificacoes')


