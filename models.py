from datetime import datetime

from app import db, bcrypt

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    email = db.Column(db.String(120), unique=True)
    pw_hash = db.Column(db.String())

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.pw_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def __str__(self):
        return self.first_name

    def check_password(self, password):
        return bcrypt.check_password_hash(self.pw_hash, password)
