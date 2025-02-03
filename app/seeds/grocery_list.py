from app.models import db, User, environment, SCHEMA, GroceryList
from sqlalchemy.sql import text


def seed_grocery_lists():
    demo_list = GroceryList(
        user_id=1,
    )
    marnie_list = GroceryList(
        user_id=2,
    )
    bobbie_list = GroceryList(
        user_id=3,
    )

    db.session.add(demo_list)
    db.session.add(marnie_list)
    db.session.add(bobbie_list)
    db.session.commit()



def undo_grocery_lists():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.grocery_lists RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM grocery_lists"))

    db.session.commit()
