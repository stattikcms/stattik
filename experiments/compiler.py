"""
from __blogsley__ import db

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(16))
    title = db.Column(db.String(256))
    slug = db.Column(db.String(256))
    block = db.Column(db.Text)
    cover = db.Column(db.String(256))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
"""

from post import Post

class Compiler:
    def compile():
        pass