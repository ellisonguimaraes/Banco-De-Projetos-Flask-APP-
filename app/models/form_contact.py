from app import db


class FormContact(db.Model):
    __tablename__ = 'form_contact'
    id = db.Column(db.Integer, primary_key=True, nullable=False)

    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    def __init__(self, name, email, message, date):
        self.name = name
        self.email = email
        self.message = message
        self.date = date