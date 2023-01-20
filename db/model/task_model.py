from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    status = db.Column(db.Boolean, unique=False, nullable=True)

    def __init__(self, name=None, status=False):
        self.name = name
        self.status = status

    def to_json(self):

        return {
            "id": self.id,
            "name": self.name,
            "status": 0 if self.status is False else 1,
        }
