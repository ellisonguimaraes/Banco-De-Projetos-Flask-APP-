from app import db


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    category = db.Column(db.String(100), nullable=False)

    tag_projeto = db.relationship('TagProjeto', back_populates='tags')

    def __init__(self, category):
        self.category = category

