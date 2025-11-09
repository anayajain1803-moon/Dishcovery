from flask import Flask, render_template, request, redirect, url_for, session
from ai_helper import suggest_recipes_with_time
import json

app = Flask(__name__)
app.secret_key = "super_secret_key"

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if username == "admin" and password == "1234":
        session['user'] = username
        return redirect(url_for('ingredients_page'))
    else:
        return render_template('login.html', error="Invalid login credentials")

@app.route('/ingredients')
def ingredients_page():
    if 'user' not in session:
        return redirect(url_for('home'))
    return render_template('ingredients.html')

@app.route('/get_recipes', methods=['POST'])
def get_recipes():
    ingredients_input = request.form.get("ingredients", "").strip()
    if not ingredients_input:
        return render_template('ingredients.html', error="Please enter ingredients")

    matched_recipes = suggest_recipes_with_time(ingredients_input)

    if not matched_recipes:
        return render_template('ingredients.html', error="No recipes found for your ingredients")

    session['recipes'] = matched_recipes
    return redirect(url_for('results_page'))

@app.route('/results')
def results_page():
    if 'user' not in session:
        return redirect(url_for('home'))

    recipes = session.get('recipes', [])

    # Add image URL for each recipe
    for r in recipes:
        if 'image' in r:
            if r['image'].startswith("http"):
                r['image_url'] = r['image']  # placeholder URLs
            else:
                r['image_url'] = url_for('static', filename=r['image'].replace('static/', ''))
        else:
            r['image_url'] = url_for('static', filename='images/default.jpg')

    return render_template('results.html', recipes=recipes)

@app.route('/recipe/<int:recipe_index>')
def recipe_page(recipe_index):
    if 'user' not in session:
        return redirect(url_for('home'))

    recipes = session.get('recipes', [])
    if recipe_index < 0 or recipe_index >= len(recipes):
        return redirect(url_for('results_page'))

    recipe = recipes[recipe_index]
    instructions = recipe.get('instructions', [
        "Step 1: Prepare ingredients.",
        "Step 2: Cook as per recipe.",
        "Step 3: Serve and enjoy!"
    ])

    return render_template('recipe.html', recipe=recipe, instructions=instructions)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

if __name__ == "__main__":
    from os import environ
    app.run(host="0.0.0.0", port=int(environ.get("PORT", 5000)))
