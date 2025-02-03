from flask.cli import AppGroup
from .users import seed_users, undo_users
from .grocery_list import seed_grocery_lists, undo_grocery_lists
from .item import seed_items, undo_items
from .grocery_list_assoc import seed_association, undo_assocation

from app.models.db import db, environment, SCHEMA

# Creates a seed group to hold our commands
# So we can type `flask seed --help`
seed_commands = AppGroup('seed')


# Creates the `flask seed all` command
@seed_commands.command('all')
def seed():
    if environment == 'production':
        # Before seeding in production, you want to run the seed undo
        # command, which will  truncate all tables prefixed with
        # the schema name (see comment in users.py undo_users function).
        # Make sure to add all your other model's undo functions below
        undo_users()
        undo_grocery_lists()
        undo_items()
        undo_assocation()
    seed_users()
    seed_grocery_lists()
    seed_items()
    seed_association()
    # Add other seed functions here


# Creates the `flask seed undo` command
@seed_commands.command('undo')
def undo():
    undo_users()
    undo_grocery_lists()
    undo_items()
    undo_assocation()
    # Add other undo functions here
