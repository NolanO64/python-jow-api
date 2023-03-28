# -*- coding: utf-8 -*-

import requests
import json



class Recipe:
    
    _ALL_ATTRIBUTES = ["id", "name", "url", "ingredients"]
    
    def __init__(self,json,simple):
        self.__json=json
        self.__simple=simple
    
    @property
    def ALL_ATTRIBUTES(self): #To make _ALL_ATTRIBUTES a read-only attribute
        return self._ALL_ATTRIBUTES
    
    def get_json(self):
        """Get raw json

        Returns:
            dict: Raw json from an API CALL
        """
        return self.__json
    
    def get_simple(self):
        """Get simple attribute

        Returns:
            bool: wheter the instance is from a 'simple' API CALL
        """
        return self.__simple
        
    def get_info(self,attributes=[]):
        """Get recipes infos

        Returns:
            list: list of infos of given recipes
        """
        data = []
        for json in self.__json:
            data.append(self.__get(json,attributes))

        return data


    @classmethod
    def __get(cls, json, attributes):
        """Get recipe infos

        Args:
            json (str): Json dictionnary of a recipe 
            attributes (list, optional): Attributes to be returned (infos on a recipe). Defaults to [] (meaning every possible attributes).

        Returns:
            dict: infos of given recipe
        """
        data = {}
        if not attributes:
            attributes = cls._ALL_ATTRIBUTES

        for att in attributes:
            data[att] = getattr(cls, "_Recipe__get_" + att)(json)

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
            {
                "name": ing["ingredient"]["name"],
                "isOptional": ing["isOptional"],
                "quantity": ing["ingredient"]["quantityPerCover"],
                "unit": cls.__get_ingredient_unit(ing),
            }
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


    _DEFAULT_LIMIT = 1000000

    @staticmethod
    def api_call(to_search, limit=0):
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

        recipes = Recipe(response_json["data"],True)
        return recipes

