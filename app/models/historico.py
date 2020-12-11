from app import db


class Historico(db.Model):
    __tablename__ = 'historicos'
    id = db.Column(db.Integer, primary_key=True, nullable=False)

    date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    users = db.relationship('User', back_populates='historicos')

    project_id = db.Column(db.Integer, db.ForeignKey('projetos.id'), nullable=False)
    projetos = db.relationship('Projeto', back_populates='historicos')

    def __init__(self, date, description, user_id, project_id):
        self.date = date
        self.description = description
        self.user_id = user_id
        self.project_id = project_id

