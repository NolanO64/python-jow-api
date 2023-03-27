# -*- coding: utf-8 -*-

import requests
import json


class Jow:
    # Settings for general Jow API calls
    _OPTION_HEADERS = {
        "accept": "*/*",
        "accept-language": "fr,fr-FR;q=0.9,en-US;q=0.8,en;q=0.7",
        # "sec-fetch-dest": "empty",
        # "sec-fetch-mode": "cors",
        # "sec-fetch-site": "same-site",
        # "Referer": "https://jow.fr/",
        # "Referrer-Policy": "strict-origin-when-cross-origin"
    }

    _OPTION_PARAMS = {"start": 1, "availabilityZoneId": "FR"}

    _POST_HEADERS = {
        "accept": "application/json",
        "accept-language": "fr",
        "content-type": "application/json",
        # "sec-ch-ua": "\"Google Chrome\";v=\"111\", \"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"111\"",
        # "sec-ch-ua-mobile": "?0",
        # "sec-ch-ua-platform": "\"Windows\"",
        # "sec-fetch-dest": "empty",
        # "sec-fetch-mode": "cors",
        # "sec-fetch-site": "same-site",
        # "x-jow-prefers-color-scheme": "light",
        # "x-jow-referrer": "https://jow.fr/cooking?search=poulet",
        # "x-jow-web-version": "7.7.0",
        "x-jow-withmeta": "1",
        # "cookie": "_gid=GA1.2.498479097.1679693171; _pin_unauth=dWlkPU9EZGlOelUyTmpBdE16Y3pOaTAwWm1RM0xXRXdZbVV0TWpZNU56STBNRGRqTVRkaw; __stripe_mid=e1736ecb-990c-4d1f-9807-fc3705f74786d55d8d; afUserId=094dc265-f800-4946-9529-a7c9ba264cc6-p; AF_SYNC=1679693171821; intercom-id-awqp4pm4=7bc274a4-da01-4882-924c-9caa68d14981; intercom-session-awqp4pm4=; intercom-device-id-awqp4pm4=a4cc9284-649c-4a5b-bd49-f78b638fc8de; __stripe_sid=ce68513f-a8e2-44fd-bf35-b482bf0857c1be21a6; JowSession=AAABhx6XoRUBDLhpJ_sdy008ZAhWwvaodxx8HhXmCzKvTS7Fhnl7_Qv4bemcOufRsCc; _derived_epik=dj0yJnU9SVFrVDVBUElRcm5jTWRObXJQdk0wR25TRFFmZkRPbjAmbj14ZU54X1Ixcm1uQ0kydk55YzJUdjZRJm09MSZ0PUFBQUFBR1FncDBJJnJtPTEmcnQ9QUFBQUFHUWdwMEkmc3A9Mg; _ga=GA1.1.1489989006.1679693171; _ga_SEH3VC5TCR=GS1.1.1679860409.11.1.1679861605.0.0.0",
        # "Referer": "https://jow.fr/",
        # "Referrer-Policy": "strict-origin-when-cross-origin"
    }

    _POST_PARAMS = {"start": "1", "availabilityZoneId": "FR"}

    _SEARCH_URL = "https://api.jow.fr/public/recipe/quicksearch"
    _RECIPE_URL = "https://jow.fr/recipes/"

    __ALL_ATTRIBUTES = ["id", "name", "url", "ingredients"]

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

        return response_json["data"]

    @staticmethod
    def get_ingredient_unit(ingredient):
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
    def get_name(recipe):
        """Get recipe name (title)

        Args:
            recipe (dict): Json dictionnary of a recipe (returned from an api call)

        Returns:
            str: recipe name
        """
        return recipe["title"]

    @staticmethod
    def get_id(recipe):
        """Get recipe id

        Args:
            recipe (dict): Json dictionnary of a recipe (returned from an api call)

        Returns:
            str: recipe id
        """
        return recipe["_id"]

    @staticmethod
    def get_url(recipe):
        """Get recipe url

        Args:
            recipe (dict): Json dictionnary of a recipe (returned from an api call)

        Returns:
            str: recipe url
        """
        return Jow._RECIPE_URL + recipe["_id"]

    @classmethod
    def get_ingredients(cls, recipe):
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
                "unit": cls.get_ingredient_unit(ing),
            }
            for ing in recipe["constituents"]
        ]
        return list_of_ingredients

    @classmethod
    def get(cls, json, attributes=[]):
        """Get recipe infos

        Args:
            json (str): Json dictionnary of a recipe (returned from an api call)
            attributes (list, optional): Attributes to be returned (infos on a recipe). Defaults to [].

        Returns:
            dict: infos of given recipe
        """
        data = {}
        if not attributes:
            attributes = cls.__ALL_ATTRIBUTES

        for att in attributes:
            data[att] = getattr(cls, "get_" + att)(json)

        return data

    @classmethod
    def get_all(cls, json_list):
        """Get recipes infos

        Args:
            json_list (list): list of Json dictionnary (returned directyl from an api call)

        Returns:
            list: list of infos of given recipes
        """
        data = []
        for json in json_list:
            data.append(Jow.get(json))

        return data
