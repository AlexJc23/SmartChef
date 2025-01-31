from datetime import datetime
from .db import db, environment, SCHEMA, add_prefix_for_prod
from sqlalchemy.dialects.sqlite import JSON


class Recipe(db.Model):
    __tablename__ = 'recipes'

    if environment == 'production':
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(500), nullable=False)
    instructions = db.Column(JSON, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'instructions': self.instructions,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
