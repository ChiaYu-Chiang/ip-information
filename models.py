from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Search(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fqdn = db.Column(db.String(255), nullable=False)
    ip = db.Column(db.String(15), nullable=False)
    time = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<Search %r>" % self.name
