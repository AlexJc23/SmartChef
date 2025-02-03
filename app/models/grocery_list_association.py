from .db import db, environment, SCHEMA, add_prefix_for_prod
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime


class GroceryListAssociation(db.Model, UserMixin):
    __tablename__ = 'grocery_list_associations'

    if environment == 'production':
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    list_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('grocery_lists.id'), ondelete='CASCADE'))
    item_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('items.id'), ondelete='CASCADE'))
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    grocery_list = db.relationship('GroceryList', back_populates='grocery_list_associations')
    item = db.relationship('Item', back_populates='grocery_list_associations')

    def to_dict(self):
        return {
            'id': self.id,
            'list_id': self.list_id,
            "item_id": self.item_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
