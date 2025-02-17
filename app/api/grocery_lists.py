from flask import Blueprint, jsonify, redirect, request
from flask_login import current_user, login_required
from app.models import Recipe, FavoriteRecipe, GroceryList, GroceryListAssociation, Item
from app import db


lists_routes = Blueprint('list', __name__)

@lists_routes.route('/')
@login_required
def grab_grocery_list():
    """
    Fetch the grocery list for logged-in user
    """
    logged_in_user = current_user.to_dict()

    users_grocery_list = db.session.query(GroceryList).filter(
        GroceryList.user_id == logged_in_user['id']
    ).first()


    if not users_grocery_list:
        return jsonify({'error': 'No grocery list found'}), 404


    users_grocery_list_dict = users_grocery_list.to_dict()

    items_in_list = db.session.query(Item).join(GroceryListAssociation).filter(
        GroceryListAssociation.list_id == users_grocery_list_dict['id']
    ).all()


    return jsonify({
        'grocery_list': users_grocery_list_dict,
        'items': [item.to_dict() for item in items_in_list]  # Ensure items are converted properly
    }), 200
