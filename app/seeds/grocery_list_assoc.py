from app.models import db, User, environment, SCHEMA, Item, GroceryListAssociation
from sqlalchemy.sql import text


def seed_association():
    list_item1 = GroceryListAssociation(list_id=1, item_id=3)
    list_item2 = GroceryListAssociation(list_id=1, item_id=1)
    list_item3 = GroceryListAssociation(list_id=2, item_id=3)
    list_item4 = GroceryListAssociation(list_id=1, item_id=4)
    list_item5 = GroceryListAssociation(list_id=1, item_id=5)
    list_item6 = GroceryListAssociation(list_id=2, item_id=6)

    db.session.add(list_item1)
    db.session.add(list_item2)
    db.session.add(list_item3)
    db.session.add(list_item4)
    db.session.add(list_item5)
    db.session.add(list_item6)

    db.session.commit()

def undo_assocation():
    if environment == 'production':
        db.session.execute(f"TRUNCATE table {SCHEMA}.grocery_list_associations RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text('DELETE FROM grocery_list_associations'))
    db.session.commit()
