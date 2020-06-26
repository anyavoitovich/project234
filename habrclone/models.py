from habrclone import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, index=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(20))
    avatar = db.Column(db.String(20), default='default.jpg')
    news = db.relationship('New', backref ='author', lazy=True)

    def __repr__(self):
        return f'пользователь: {self.username}, email {self.email}'
    def set_password(self, user_passw):
        self.password = generate_password_hash(user_passw)

    def check_password(self, user_passw):
        return check_password_hash(self.password, user_passw)

class New(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    article = db.Column(db.String(100))
    puplish_date = db.Column(db.DateTime, default=datetime.utcnow)
    body = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))




@login.user_loader
def load_user(id):
        return User.guery.get(int(id))