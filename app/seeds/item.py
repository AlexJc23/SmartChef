from app.models import db, User, environment, SCHEMA, Item
from sqlalchemy.sql import text


def seed_items():
    item1 = Item(name='Milk')
    item2 = Item(name='Eggs')
    item3 = Item(name='Vanilla Extract')
    item4 = Item(name='Self-rising Flour')
    item5 = Item(name='Granulated Sugar')
    item6 = Item(name='Light Brown Sugar')


    db.session.add(item1)
    db.session.add(item2)
    db.session.add(item3)
    db.session.add(item4)
    db.session.add(item5)
    db.session.add(item6)
    db.session.commit()

def undo_items():
    if environment == 'production':
        db.session.execute(f"TRUNCATE table {SCHEMA}.items RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text('DELETE FROM items'))
    db.session.commit()
