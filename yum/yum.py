import json
import re
import sys
import yum.Parser as Parser
import yum.connector as connector
import yum.food as food
import yum.state as state
import yum.CONSTANTS as CONST

from random import randint

class Yum():
    def __init__(self, api_id, api_key, server):
        """
        Constructor of communicator with Yummly
        :param api_id: Application ID
        :param api_key: Application key
        """
        self.api_id = api_id
        self.api_key = api_key
        self.params = {}
        self.conn = connector.Client(api_id, api_key)
        self.server = server

    def recipe(self, diet, allergy, cuisine, exclude_cuisine, ingredient, exclude_ingredient, holiday, exclude_holiday, phrase, file, config):
        """
        Generate recipes with difficulty computed from your level
        :param diet: Diets
        :param allergy: Allergies
        :param cuisine: National cuissines
        :param exclude_cuisine: Excluding national cuisines
        :param ingredient: Ingredients
        :param exclude_ingredient: Excluding ingredients
        :param holiday: Holiday recipes
        :param exclude_holiday: Excluding holiday recipes
        :param phrase: Name of the recipe
        :param file: Config file
        :return generated food
        """
        self.setAllParameters(diet, allergy,
                              cuisine, exclude_cuisine,
                              ingredient, exclude_ingredient,
                              holiday, exclude_holiday,
                              phrase,
                              file, config)
        id = self.randomId()

        if not id:
            return None

        result = self.conn.get(id)
        actual = food.Food(result.json())
        self.saveRecipe(actual, config)
        return actual

    def saveRecipe(self, food, config):
        """
        Save the recipe to recipe.cfg file
        :param food: food to save
        :param config: configuration file
        """
        fields = ['name','url', 'ingredients','picture']
        ingredients = ",".join(food.ingredients)
        values = [
            food.name,
            food.url,
            ingredients,
            food.picture
        ]
        jsonData = self.buildJson(fields,values)
        url = self.server
        url += 'saverecipe'

        password = Parser.getPassword(None, config)
        connector.post(url, jsonData, password)
        Parser.updateSave(CONST.RECIPE_FILE, 'recipe', fields, values)

    def buildJson(self, fields, values):
        """
        Builds json
        :param fields: fields for json
        :param values: values for fields in json
        :return: json
        """
        i = 0
        data = {}
        for field in fields:
            data[field] = values[i]
            i += 1

        json_data = json.dumps(data)
        return json_data

    def loadParamsFromFile(self, config):
        """
        Load user's parameters from the configuration file
        :param config: path to config file
        """
        diet = Parser.getParameter(config, 'diet')
        allergy = Parser.getParameter(config, 'allergy')
        cuisine = Parser.getParameter(config, 'cuisine')
        exclude_cuisine = Parser.getParameter(config, 'exclude_cuisine')
        ingredient = Parser.getParameter(config, 'ingredient')
        exclude_ingredient = Parser.getParameter(config, 'exclude_ingredient')
        holiday = Parser.getParameter(config, 'holiday')
        exclude_holiday = Parser.getParameter(config, 'exclude_holiday')
        phrase = Parser.getParameter(config, 'phrase')
        self.setAllParameters(diet, allergy,
                              cuisine, exclude_cuisine,
                              ingredient, exclude_ingredient,
                              holiday, exclude_holiday,
                              phrase,
                              False, config)


    def setAllParameters(self, diet, allergy, cuisine, exclude_cuisine, ingredient, exclude_ingredient, holiday, exclude_holiday, phrase, file, config):
        """
        the main function for building the parameters
        :param diet: Diets
        :param allergy: Allergies
        :param cuisine: National cuissines
        :param exclude_cuisine: Excluding national cuisines
        :param ingredient: Ingredients
        :param exclude_ingredient: Excluding ingredients
        :param holiday: Holiday recipes
        :param exclude_holiday: Excluding holiday recipes
        :param phrase: Name of the recipe
        :param file: Config file
        """
        if(file):
            self.loadParamsFromFile(config)
        else:
            self.setParameter(diet, 'diet', 'allowedDiet')
            self.setParameter(allergy, 'allergy', 'allowedAllergy')
            self.setParameter(cuisine, 'cuisine', 'allowedCuisine')
            self.setParameter(exclude_cuisine, 'cuisine', 'excludedCuisine')
            self.setParameter(ingredient, 'ingredient', 'allowedIngredient')
            self.setParameter(exclude_ingredient, 'ingredient', 'excludedIngredient')
            self.setParameter(holiday, 'holiday', 'allowedHoliday')
            self.setParameter(exclude_holiday, 'holiday', 'excludedHoliday')
            self.setMatchingPhrase(phrase)

    def setMatchingPhrase(self, phrase):
        """
        Set parameter for matching the phrase of the recipe
        :param phrase: The name or the part of the name of recipe
        """
        self.params['q'] = phrase

    def randomId(self):
        """
        Get random id from the founded food
        :return: ID of the choosen food
        """
        self.buildParams()
        result = self.conn.search(self.params)
        index = randint(0, CONST.MAX_RESULTS - 1)
        id = None
        try:
            id = result.json()['matches'][index]['id']
        except:
            return self.noMatch()
        return id

    def buildParams(self):
        """Set General Parameters for the Request"""
        user = state.State(0,False)
        self.setTime( self.calcTime(user) )

    def setTime(self, minutes):
        """
        Set the maximum time for cooking
        :param minutes: Time in minutes
        """
        seconds = minutes * 60
        self.params['maxTotalTimeInSeconds'] = seconds

    def calcTime(self, user):
        """
        Very sophisticated super ultra intelligent calculation of time for cooking
        :param user: The user is representation of the actual state
        :return: calculated time
        """
        if(user.level == 0):
            return 1
        else:
            return user.level * user.level

    def setParameter(self, parameters, metakey, field):
        """
        Set the parameters depending on metadata
        :param parameters:  Parameter
        :param metakey: Key in metadata
        :param field: Value in metadata
        """
        if(parameters != None):
            allParams = parameters.split(',')
            raw = self.conn.getMeta(metakey)
            metadata = self.parseMeta(raw)
            finalParams = []
            for p in allParams:
                searchValue = self.getSearchValue(metadata, p)

                # no match with metadata
                if searchValue == None:
                    self.noMatch()

                finalParams.append(searchValue)
            self.params[field] = finalParams

    def getSearchValue(self, response, short):
        """
        Get metadata name
        :param response: Response from yummly
        :param short: Short description of metadata
        :return: real metadata name
        """
        for metaline in response:
            hit = short.strip()
            if 'description' in metaline:
                if (re.search(r'^'+hit, metaline.get('description'), re.IGNORECASE)):
                    return metaline.get('searchValue')
            else:
                if (re.search(r'^'+hit, metaline.get('shortDescription'), re.IGNORECASE)):
                    return metaline.get('searchValue')

    def parseMeta(self, response):
        """
        Support function to achieve parsing the response including metadata
        :param response: response to parse
        :return: parsed json
        """
        text = response.text
        start = text.index('[')
        end = text.rfind(']') + 1
        parsed = text[start:end]
        return json.loads(parsed)

    def noMatch(self):
        """
        Exit application because of the error
        """
        print("Sorry, I can't find any recipe that fulfil you requirements.")
        return None


