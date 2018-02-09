from yum import Parser

class Food:
    """
    Class representing food from Yummly
    """
    def __init__(self, data):
        """
        Constructor of Yummly food
        :param data: json from Yummly client including single food information
        """
        if data != None:
            self.name = data['name']
            self.url = data.get('source')['sourceRecipeUrl']
            self.ingredients = data.get('ingredientLines')

            # set image URL if exists
            if 'hostedLargeUrl' in data['images'][0]:
                self.picture = data['images'][0]['hostedLargeUrl']
            elif 'hostedMediumUrl' in data['images'][0]:
                self.picture = data['images'][0]['hostedMediumUrl']
            elif 'hostedSmallUrl' in data['images'][0]:
                self.picture = data['images'][0]['hostedSmallUrl']
            else:
                self.picture = "https://i.pinimg.com/originals/8e/d1/fb/8ed1fb0dfdfdc88c6b2e0874585bd08c.jpg"

    def text(self):
        """
        Simple text representation of food
        :return: Food as String
        """
        result = self.name + '\n'
        result += '\nIngredients: \n'
        for ingredient in self.ingredients:
            result += ingredient + '\n'
        result += '\nStep-by-step: ' + self.url
        return result

    def load(self, file):
        """
        Load food from recipe file - last generated user's food
        :param file: recipe file (default: recipe.cfg)
        :return: Food
        """
        self.name = Parser.get(file,'recipe','name')
        self.ingredients = Parser.get(file,'recipe','ingredients')
        self.url = Parser.get(file,'recipe','url')
        self.picture = Parser.get(file,'recipe','picture')
        return self
