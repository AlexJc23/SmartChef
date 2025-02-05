from flask import Blueprint, jsonify, redirect, request
# from app import db
from flask_login import current_user, login_required
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()


test_case = ['onion', 'rice', 'chicken', 'mushroom soup' ]

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

class Chef(BaseModel):
    name: str
    ingredients: list[str]
    ingredients_without_measurments: list[str]
    instructions: list[str]

completion = client.beta.chat.completions.parse(
    model='gpt-4o-mini-2024-07-18',
    messages=[
        {'role': 'system', 'content': 'You are an expert at structured data extraction. You will be given a list of ingrediants and give a recipe back in the given structure.'},
        {'role': 'user', 'content': "".join(test_case)}
    ],
    response_format=Chef,
)

recipe = completion.choices[0].message.parsed


