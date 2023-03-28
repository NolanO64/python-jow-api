# -*- coding: utf-8 -*-

import requests
import json


class Ingredient:
    def __init__(self, name, quantity, unit, isOptional):
        self.name = name
        self.quantity = quantity
        self.unit = unit
        self.isOptional = isOptional


class JowResult:
    def __init__(
        self,
        id=None,
        url=None,
        name=None,
        ingredients=None,
        imageUrl=None,
        videoUrl=None,
        json=None,
        description=None,
        preparationTime=None,
        preparationExtraTimePerCover=None,
        cookingTime=None,
    ):
        self.id = id
        self.url = url
        self.name = name
        self.ingredients = ingredients
        self.imageUrl = imageUrl
        self.videoUrl = videoUrl
        self.description = description
        self.preparationTime = preparationTime
        self.cookingTime = cookingTime
        self.preparationExtraTimePerCover = preparationExtraTimePerCover
        self.json = json

    # To be defined...

    # def get_info(self):
    # return Jow.scrap_data([self])[0]


class Recipe:
    # To be defined...
    pass


class Jow:
    # Settings for general Jow API calls
    _OPTION_HEADERS = {
        "accept": "*/*",
        "accept-language": "fr,fr-FR;q=0.9,en-US;q=0.8,en;q=0.7",
    }

    _OPTION_PARAMS = {"start": 1, "availabilityZoneId": "FR"}

    _POST_HEADERS = {
        "accept": "application/json",
        "accept-language": "fr",
        "content-type": "application/json",
        "x-jow-withmeta": "1",
    }

    _POST_PARAMS = {"start": "1", "availabilityZoneId": "FR"}

    _SEARCH_URL = "https://api.jow.fr/public/recipe/quicksearch"
    _RECIPE_URL = "https://jow.fr/recipes/"
    _STATIC_URL = "https://static.jow.fr/"

    _DEFAULT_LIMIT = 1000000

    __ALL_ATTRIBUTES = [
        "id",
        "name",
        "url",
        "videoUrl",
        "imageUrl",
        "ingredients",
        "description",
        "preparationExtraTimePerCover",
        "cookingTime",
        "preparationTime",
    ]

    @classmethod
    def search(cls, to_search, limit=0):
        """Performs a search on Jow.fr

        Args:
            to_search (str): String to be searched.
            limit (int, optional): Maximum number of recipe fetched. Defaults to 0 (no limit).

        Returns:
            response (dict): Json containing the result of the api call
        """

        params_opt = Jow._OPTION_PARAMS
        params_opt["query"] = to_search

        params_opt["limit"] = limit if limit != 0 else Jow._DEFAULT_LIMIT

        response = requests.options(
            Jow._SEARCH_URL, headers=Jow._OPTION_HEADERS, params=params_opt
        )

        if response.status_code != 204:
            raise ValueError("ERROR IN OPTION REQUEST")

        params_post = Jow._POST_PARAMS
        params_post["query"] = to_search
        params_post["limit"] = limit if limit != 0 else Jow._DEFAULT_LIMIT

        response = requests.post(
            Jow._SEARCH_URL, headers=Jow._POST_HEADERS, params=params_post, data="{}"
        )

        if response.status_code != 200:
            raise ValueError("ERROR IN POST REQUEST")

        response_json = json.loads(response.text)

        recipes = cls.__get_info(response_json["data"])

        return recipes

    # To be defined...

    # @staticmethod
    # def scrap_data(s_result):
    #     pass

    @classmethod
    def __get_info(cls, recipes):
        """Get recipes infos from search query

        Args:
            recipes (list): list of Json dictionnaries returned from search query

        Returns:
            list: list of JowResult from given recipes
        """
        data = []

        for recipe in recipes:
            data.append(cls.__get(recipe))

        return data

    @classmethod
    def __get(cls, Json):
        """Get recipe infos

        Args:
            json (str): Json dictionnary returned from search query

        Returns:
            JowResult: infos of given recipe
        """
        data = JowResult()

        for att in cls.__ALL_ATTRIBUTES:
            setattr(data, att, getattr(cls, "_Jow__get_" + att)(Json))

        data.json = json.dumps(Json)

        return data

    @classmethod
    def __get_ingredients(cls, recipe):
        """Get ingredient info

        Args:
            recipe (dict): Json dictionnary of a recipe (returned from an api call)

        Returns:
            list: list of dictionnary containing infos on each ingredient of a given recipe
        """

        list_of_ingredients = [
            Ingredient(
                ing["ingredient"]["name"],
                ing["ingredient"]["quantityPerCover"],
                cls.__get_ingredient_unit(ing),
                ing["isOptional"],
            )
            for ing in recipe["constituents"]
        ]

        return list_of_ingredients

    @staticmethod
    def __get_ingredient_unit(ingredient):
        """Get unit of an ingredient

        Args:
            ingredient (dict): Json dictionnary of constituent (returned from an api call)

        Returns:
            str: best fiting measuring unit of a given ingredient (the one shown on the website)
        """

        unit_id = ingredient["unit"]["id"]
        if ingredient["ingredient"]["naturalUnit"]["_id"] == unit_id:
            return ingredient["ingredient"]["naturalUnit"]["name"]
        else:
            for unit in ingredient["ingredient"]["alternativeUnits"]:
                if unit["unit"]["_id"] == unit_id:
                    return unit["unit"]["name"]

    @staticmethod
    def __get_name(recipe):
        """Get recipe name (title)

        Args:
            recipe (dict): Json dictionnary of a recipe (returned from an api call)

        Returns:
            str: recipe name
        """
        return recipe["title"]

    @staticmethod
    def __get_id(recipe):
        """Get recipe id

        Args:
            recipe (dict): Json dictionnary of a recipe (returned from an api call)

        Returns:
            str: recipe id
        """
        return recipe["_id"]

    @staticmethod
    def __get_url(recipe):
        """Get recipe url

        Args:
            recipe (dict): Json dictionnary of a recipe (returned from an api call)

        Returns:
            str: recipe url
        """
        return Jow._RECIPE_URL + recipe["_id"]

    @staticmethod
    def __get_videoUrl(recipe):
        """Get video recipe url

        Args:
            recipe (dict): Json dictionnary of a recipe (returned from an api call)

        Returns:
            str: video recipe url
        """
        return Jow._STATIC_URL + recipe["videoUrl"]

    @staticmethod
    def __get_imageUrl(recipe):
        """Get image recipe url

        Args:
            recipe (dict): Json dictionnary of a recipe (returned from an api call)

        Returns:
            str: image recipe url
        """
        return Jow._STATIC_URL + recipe["imageUrl"]

    @staticmethod
    def __get_description(recipe):
        """Get recipe description

        Args:
            recipe (dict): Json dictionnary of a recipe (returned from an api call)

        Returns:
            str: recipe description
        """
        return recipe["description"]

    @staticmethod
    def __get_preparationTime(recipe):
        """Get recipe preparation time

        Args:
            recipe (dict): Json dictionnary of a recipe (returned from an api call)

        Returns:
            str: recipe preparation time
        """
        return recipe["preparationTime"]

    @staticmethod
    def __get_cookingTime(recipe):
        """Get recipe cooking time

        Args:
            recipe (dict): Json dictionnary of a recipe (returned from an api call)

        Returns:
            str: recipe cooking time
        """
        return recipe["cookingTime"]

    @staticmethod
    def __get_preparationExtraTimePerCover(recipe):
        """Get recipe preparation extra time per cover

        Args:
            recipe (dict): Json dictionnary of a recipe (returned from an api call)

        Returns:
            str: recipe preparation extra time per cover
        """
        return recipe["preparationExtraTimePerCover"]
