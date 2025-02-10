from flask import Blueprint, jsonify, redirect, request
# from app import db
from flask_login import current_user, login_required
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
from app.models import Recipe
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
    ingredients = request.json.get('ingredients')
    # print(ingredients)

    if not ingredients:
        return jsonify({'error': 'Please provide list of ingredients'}), 404

    try:
        completion = client.beta.chat.completions.parse(
            model='gpt-4o-mini-2024-07-18',
            messages=[
                {'role': 'system', 'content': 'You are an expert at structured data extraction. You will be given a list of ingrediants and give a recipe back in the given structure.'},
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
        ingrediants = pickle.dumps(recipe["ingredients"])
    )
    db.session.add(new_recipe)
    db.session.commit()
    return jsonify({
        'id': new_recipe.id,
        'name': new_recipe.name,
        'instructions': recipe["instructions"],  # Unpickled
        'ingredients': recipe["ingredients"]  # Unpickled
    }), 200
