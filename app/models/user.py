from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from app import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    specialty = db.Column(db.String(200), nullable=False)
    summary = db.Column(db.Text)
    ref = db.Column(db.String(400))
    type_user = db.Column(db.Integer, nullable=False)

    pessoa_projeto = db.relationship('PessoaProjeto', back_populates='users')

    def __init__(self, name, email, password, specialty, summary, ref, type_user):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)
        self.specialty = specialty
        self.summary = summary
        self.ref = ref
        self.type_user = type_user

    def verify_password(self, password):
        return check_password_hash(self.password, password)
