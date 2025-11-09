import json

# Load all recipes from JSON file
with open('recipes.json', 'r', encoding='utf-8') as f:
    ALL_RECIPES = json.load(f)

def suggest_recipes_with_time(ingredients_input):
    """
    Suggest recipes based on comma-separated ingredients input.
    Returns list of matching recipes.
    """
    if not ingredients_input:
        return []

    user_ingredients = [i.strip().lower() for i in ingredients_input.split(',')]
    matched = []

    for recipe in ALL_RECIPES:
        recipe_ingredients = [ri.lower() for ri in recipe.get('ingredients', [])]
        if any(ing in recipe_ingredients for ing in user_ingredients):
            matched.append(recipe)

    return matched
