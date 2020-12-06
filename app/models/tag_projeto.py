from app import db


class TagProjeto(db.Model):
    __tablename__ = 'tag_projeto'
    id = db.Column(db.Integer, primary_key=True, nullable=False)

    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), nullable=False)
    tags = db.relationship('Tag', back_populates='tag_projeto')

    project_id = db.Column(db.Integer, db.ForeignKey('projetos.id'), nullable=False)
    projetos = db.relationship('Projeto', back_populates='tag_projeto')