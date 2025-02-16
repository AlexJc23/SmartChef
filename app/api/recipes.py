from flask import Blueprint, jsonify, redirect, request
# from app import db
from flask_login import current_user, login_required
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
from app.models import Recipe, FavoriteRecipe
import pickle
from app import db
import os

load_dotenv()



client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


class Chef(BaseModel):
    name: str
    ingredients: list[str]
    ingredients_without_measurments: list[str]
    instructions: list[str]

recipe_routes = Blueprint('recipe', __name__)

@recipe_routes.route('/generate', methods=['POST'])
def generate_recipe():
    """
    Fetch a generated recipe with given ingredients
    """
    ingredients = request.json.get('ingredients')


    if not ingredients:
        return jsonify({'error': 'Please provide list of ingredients'}), 404

    try:
        completion = client.beta.chat.completions.parse(
            model='gpt-4o-mini-2024-07-18',
            messages=[
                {'role': 'system', 'content': 'You are an expert at structured data extraction. You will be given a list of ingredients and give a real recipe back with the given ingredients in the given structure.'},
                {'role': 'user', 'content': "".join(ingredients)}
            ],
            response_format=Chef,
        )

        recipe = completion.choices[0].message.parsed

        return jsonify({
            'name': recipe.name,
            'ingredients': recipe.ingredients,
            'ingredients_without_measurments': recipe.ingredients_without_measurments,
            'instructions': recipe.instructions
        }), 200

    except Exception as e:
        return jsonify({'error': f'Error generating recipe: {str(e)}'}), 500


@recipe_routes.route('/add', methods=['POST'])
def add_recipe():
    """
    Add a recipe into db
    """
    recipe = request.json.get('recipe')

    if not recipe:
        return jsonify({'error': 'Please provide a recipe'}), 404

    new_recipe = Recipe(
        name = recipe['name'],
        instructions = pickle.dumps(recipe["instructions"]),
        ingredients = pickle.dumps(recipe["ingredients"]),
        ingredients_without_measurments = pickle.dumps(recipe['ingredients_without_measurments'])
    )
    db.session.add(new_recipe)
    db.session.commit()
    return jsonify({
        'id': new_recipe.id,
        'name': new_recipe.name,
        'instructions': recipe["instructions"],
        'ingredients': recipe["ingredients"],
        'ingredients_without_measurments': recipe['ingredients_without_measurments']
    }), 200



@recipe_routes.route('/favorite/<int:recipe_id>', methods=['POST'])
@login_required
def add_favorite_recipe(recipe_id):
    logged_in_user = current_user.to_dict()

    is_in_favs = db.session.query(FavoriteRecipe).filter(
        FavoriteRecipe.user_id == logged_in_user['id'],
        FavoriteRecipe.recipe_id == recipe_id
    ).first()

    if is_in_favs:
        return jsonify({'error': "Recipe is already in your favorites."})


    recipe_by_id = db.session.query(Recipe).filter(
        Recipe.id == recipe_id
    ).first()

    if not recipe_by_id:
        return {"error": 'Recipe could not be found.'}, 404

    try:
        add_to_favs = FavoriteRecipe(
            user_id = logged_in_user['id'],
            recipe_id = recipe_id
        )
        db.session.add(add_to_favs)
        db.session.commit()
        return jsonify({'Message': "Successfully added to favorites"})

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error adding to favorites {str(e)}'})


@recipe_routes.route('/remove/<int:recipe_id>', methods=['DELETE'])
@login_required
def remove_fav_recipe(recipe_id):
    logged_in_user = current_user.to_dict()


    is_in_favs = db.session.query(FavoriteRecipe).filter(
        FavoriteRecipe.user_id == logged_in_user['id'],
        FavoriteRecipe.recipe_id == recipe_id
    ).first()

    if not is_in_favs:
        return jsonify({'error': "Recipe Could not be found in favorites."}), 404

    try:
        db.session.delete(is_in_favs)
        db.session.commit()
        return jsonify({"Message": "Recipe was removed from favorites successfully."}), 200

    except Exception as e:
        return jsonify({'error': f'Error removing recipe from favorites {str(e)}'})
