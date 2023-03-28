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

recipes_json = Jow.api_call("poulet rôti",40)
recipe_dict = Jow.get_all(recipes_json)

print(recipe_dict)

```
The `api_call` function takes a search query as input, with an optional limit parameter,  and returns the raw JSON response from the Jow.fr API. To obtain the recipe data in a more readable format, you can use the `get` or `get_all` methods of the Jow class provided by the package.

The get_all method takes the raw JSON response from the api_call function as input and returns a list of dictionaries, with each dictionary representing a recipe. Each recipe dictionary contains the following keys :


* `id` : The ID of the recipe.
* `name` : The name of the recipe.
* `url` : The URL of the recipe on Jow.fr.
* `ingredients` : A list of dictionaries where each dictionary corresponds to an ingredient used in the recipe and contains the following keys:
    * `name` : The name of the ingredient.
    * `quantity` : The quantity of the ingredient needed for the recipe.
    * `unit` : The unit of measurement for the quantity of the ingredient.
    * `isOptional` : A boolean value indicating whether the ingredient is optional or not.



## License

This package is licensed under the [MIT License](https://choosealicense.com/licenses/mit/).


## Disclaimer
This package is not affiliated with Jow.fr in any way. The data is retrieved using publicly available APIs, and the package does not guarantee the accuracy of the information provided. Please use this package at your own risk.
