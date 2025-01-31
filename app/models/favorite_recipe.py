from datetime import datetime
from .db import db, environment, SCHEMA, add_prefix_for_prod


class FavoriteRecipe(db.Model):
    __tablename__ = 'favorite_recipes'

    if environment == 'production':
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('users.id'), ondelete='CASCADE'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('recipes.id'), ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, nullable=False)


    users = db.relationship('User', back_populates='favorite_recipes')
    recipes = db.relationship('Recipe', back_populates='favorite_recipes')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'recipe_id': self.recipe_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
