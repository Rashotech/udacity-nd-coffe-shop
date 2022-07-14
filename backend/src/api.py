import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)


db_drop_and_create_all()

# ROUTES
@app.route('/drinks')
def get_all_drinks():
    all_drinks = Drink.query.all()
    drinks = [drink.short() for drink in all_drinks]
    return jsonify({
        'success': True,
        'drinks': drinks
    })

@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drink_details():
    drinks = [drink.long() for drink in Drink.query.all()]

    return jsonify({
        'success': True,
        'drinks': drinks
    })

@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink():
    body = request.get_json()
    title = body.get("title", None)
    recipe = body.get("recipe", None)

    print(title)
      
    #Validate Request Body
    if(title is None or recipe is None):
        abort(422)

    try:
        # Serialize Recipe
        recipe_json = json.dumps(recipe)

        #Insert into the database
        drink = Drink(title=title, recipe=recipe_json)
        drink.insert()
            
        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        })
    except Exception as e:
        print(e)
        abort(400)

@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(id):
    drink = Drink.query.get(id)
    if drink is None:
        abort(404)

    body = request.get_json()
    title = body.get("title", None)
    recipe = body.get("recipe", None)

    try:
        if 'title' in body:
            drink.title = title

        if 'recipe' in body:
            drink.recipe = json.dumps(recipe)

        drink.update()

        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        })
    except Exception as e:
        print(e)
        abort(400)

@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(id):
    drink = Drink.query.get(id)
    if drink is None:
        abort(404)

    try:
        drink.delete()

        return jsonify({
            'success': True,
            'delete': drink.id
        })

    except Exception as e:
        print(e)
        abort(400)


# Error Handling
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422

@app.errorhandler(400)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad Request"
    }), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "success": False,
        'error': 500,
        "message": "Internal server error"
    }), 500

@app.errorhandler(AuthError)
def return_AuthError(error):
    response = jsonify(error.error)
    response.status_code = error.status_code
    return response