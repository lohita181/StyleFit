from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id         = db.Column(db.Integer, primary_key=True)
    email      = db.Column(db.String(255), unique=True, nullable=False)
    password   = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    wardrobe   = db.relationship('WardrobeItem', backref='owner', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.email}>'


class WardrobeItem(db.Model):
    __tablename__ = 'wardrobe_items'

    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    filename   = db.Column(db.String(255), nullable=False)
    filepath   = db.Column(db.String(500), nullable=False)   # web-relative path for <img src>
    type       = db.Column(db.String(10),  nullable=False)   # 'top' or 'bottom'
    occasion   = db.Column(db.String(50))                    # ML predicted label
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<WardrobeItem {self.type} - {self.occasion}>'