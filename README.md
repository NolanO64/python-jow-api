# Jow API

This is a Python package that allows you to search for recipes on [Jow.fr](https://Jow.fr). The package provides an easy-to-use interface to search for recipes and fetch information about them.

## Installation

You can install the package using [pip](https://pip.pypa.io/en/stable/) : 

```bash
pip install jow-api
```

## Usage
The package provides convenient functions for searching and obtaining recipe information. Here's an example:

```python
from jow_api import Jow

# Perform a search for recipes containing the word "poulet"
recipes = Jow.search("poulet", limit=5)

# Loop through each recipe in the results and print its attributes
for recipe in recipes:
    print(f"ID: {recipe.id}")
    print(f"Name: {recipe.name}")
    print(f"URL: {recipe.url}")
    print(f"Description: {recipe.description}")
    print(f"Preparation time: {recipe.preparationTime}")
    print(f"Cooking time: {recipe.cookingTime}")
    print(f"Preparation extra time per cover: {recipe.preparationExtraTimePerCover}")
    print(f"Covers count: {recipe.coversCount}")
    print("Ingredients:")
    for ingredient in recipe.ingredients:
        print(f"\t{ingredient.name}: {ingredient.quantity} {ingredient.unit}")
        if ingredient.isOptional:
            print("\t(optional)")
    print()

```
The Jow.search() function takes a search query as input, with an optional limit parameter, and returns a list of JowResult objects. Each JowResult object contains information about a single recipe, including its ID, name, URL on Jow.fr, and a list of ingredients.

Each JowResult object contains the following attributes:

- `id` : The ID of the recipe.
- `name` : The name of the recipe.
- `url` : The URL of the recipe on Jow.fr.
- `ingredients` : A list of Ingredient objects, each of which represents an ingredient used in the recipe.
- `imageUrl` : The URL of the recipe image on Jow.fr.
- `videoUrl` : The URL of the recipe video on Jow.fr.
- `description` : A short description of the recipe.
- `preparationTime` : The time required to prepare the recipe (in minutes).
- `preparationExtraTimePerCover` : The extra time required to prepare the recipe for each additional serving.
- `cookingTime` : The time required to cook the recipe (in minutes).

Each Ingredient object contains the following attributes:

- `name` : The name of the ingredient.
- `quantity` : The quantity of the ingredient needed for the recipe.
- `unit` : The unit of measurement for the quantity of the ingredient.
- `isOptional` : A boolean value indicating whether the ingredient is optional or not.

## License

This package is licensed under the [MIT License](https://choosealicense.com/licenses/mit/).


## Disclaimer
This package is not affiliated with Jow.fr in any way. The data is retrieved using publicly available APIs, and the package does not guarantee the accuracy of the information provided. Please use this package at your own risk.
