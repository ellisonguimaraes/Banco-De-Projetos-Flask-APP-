from app import db


class Projeto(db.Model):
    __tablename__ = 'projetos'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    summary = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    area = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(300))
    contact_email = db.Column(db.String(100), nullable=False)
    active = db.Column(db.Integer, nullable=False)
    pdf_file = db.Column(db.Text)
    images_file = db.Column(db.Text)

    pessoa_projeto = db.relationship('PessoaProjeto', back_populates='projetos')
    tag_projeto = db.relationship('TagProjeto', back_populates='projetos')
    historicos = db.relationship('Historico', back_populates='projetos')
    notificacoes = db.relationship('Notificacao', back_populates='projetos')

    def __init__(self, status, title, summary, date, area, url, contact_email, active):
        self.status = status
        self.title = title
        self.summary = summary
        self.date = date
        self.area = area
        self.url = url
        self.contact_email = contact_email
        self.active = active

