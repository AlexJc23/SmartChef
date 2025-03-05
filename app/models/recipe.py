from datetime import datetime
from .db import db, environment, SCHEMA, add_prefix_for_prod



class Recipe(db.Model):
    __tablename__ = 'recipes'

    if environment == 'production':
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(500), nullable=False, unique=True)
    ingredients = db.Column(db.String(2000), nullable=False)
    ingredients_without_measurments = db.Column(db.String(2000), nullable=False)
    instructions = db.Column(db.String(2000), nullable=False)
    details = db.Column(db.String(5000), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    favorite_recipes = db.relationship('FavoriteRecipe', back_populates='recipe', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'ingredients': self.ingrediants,
            'details': self.details,
            "ingredients_without_measurments": self.ingredients_without_measurments,
            'instructions': self.instructions,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
