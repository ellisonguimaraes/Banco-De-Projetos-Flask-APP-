from app import db


class Projeto(db.Model):
    __tablename__ = 'projetos'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    summary = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date, nullable=False)
    area = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(300))
    contact_email = db.Column(db.String(100), nullable=False)
    active = db.Column(db.Integer, nullable=False)
    pdf_file = db.Column(db.Text)
    images_file = db.Column(db.Text)

    pessoa_projeto = db.relationship('PessoaProjeto', back_populates='projetos')

