from flask import Blueprint, jsonify, redirect, request
# from app import db
from flask_login import current_user, login_required
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
from app.models import Recipe, Item, GroceryListAssociation, GroceryList
from app import db



item_routes = Blueprint('item', __name__)


@item_routes.route('/add', methods=['POST'])
def add_item():
    """
    Add new item in db
    """
    items = request.json.get('items')

    if not items:
        return jsonify({'error': 'No items were found'}), 404


    try:

        new_items = []

        for item in items:
            items_by_name = db.session.query(Item).filter(Item.name == item).first()

            if not items_by_name:
                new_item = Item(
                    name = item.lower()
                )
                db.session.add(new_item)
                new_items.append(item)

        if new_items:
            db.session.commit()
            return jsonify({'success': 'Items added', 'added_items': new_items}), 200
        else:
            return jsonify({'message': 'No new items were added'}), 200


    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error adding Items: {str(e)}'})


@item_routes.route('/associate/<int:list_id>', methods=['POST'])
@login_required
def item_to_grocery_list(list_id):
    """
    Link Item to user grocery List
    """
    current_logged_user = current_user.to_dict()

    if not current_logged_user:
        return jsonify({'error': "No user is found."})

    item = request.json.get('item')

    item_by_name = db.session.query(Item).filter(Item.name == item).first()

    if not item_by_name:
        return jsonify({'error': "Item isnt in database."}), 404

    check_if_on_list = db.session.query(GroceryListAssociation).filter(GroceryListAssociation.item_id == item_by_name.id).first()

    if not check_if_on_list:
        add_to_list = GroceryListAssociation(
            list_id = list_id,
            item_id = item_by_name.id
        )
        db.session.add(add_to_list)
        db.session.commit()
    else:
        return jsonify({'error': "Item is already on grocery list."})
    return jsonify({"message": "Item added to grocery list."})

@item_routes.route('/remove/<int:list_id>/<int:item_id>', methods=['DELETE'])
@login_required
def remove_item_from_grocery_list(list_id, item_id):
    if not current_user:
        return jsonify({'error': 'User must be logged in to remove items off of grocery list.'}), 401

    # Ensure the list belongs to the logged-in user
    user_list = GroceryList.query.filter_by(id=list_id, user_id=current_user.id).first()
    if not user_list:
        return jsonify({"error": "Forbidden: You do not own this list"}), 403

    associated_item = GroceryListAssociation.query.filter_by(list_id=list_id, item_id=item_id).first()

    if not associated_item:
        return jsonify({'error': 'Item does not exist in grocery list'}), 404

    db.session.delete(associated_item)
    db.session.commit()
    return jsonify({"message": "Item successfully removed from List"}), 200
