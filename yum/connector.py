import requests
import yum.CONSTANTS as CONST

# URLs for Yummly
URL_BASE = 'http://api.yummly.com/v1/api'
URL_RECIPES = URL_BASE + '/recipes'
URL_METADATA = URL_BASE + '/metadata/'
URL_SINGLE = URL_BASE + '/recipe/'

class Client():
    """
    The class for connector that provides communication with Yummly
    """

    def __init__(self, api_id, api_key):
        """
        Constructor for Yummly client
        :param api_id: Application id from Yummly
        :param api_key: Application key from Yummly
        """
        self.api_id = api_id
        self.api_key = api_key

    def search(self, parameters):
        """
        Seachers food from Yummly using filters
        :param parameters: Parameters for filters
        :return: Founded food
        """

        # searching parameters
        params = parameters

        # amount of searched food
        params['maxResult'] = CONST.MAX_RESULTS

        headers = {
            'X-Yummly-App-ID': self.api_id,
            'X-Yummly-App-Key': self.api_key,
        }

        result = requests.get(URL_RECIPES, params=params, headers=headers)
        return result

    def get(self, id):
        """
        Get single food by id
        :param id: id of the food from Yummly
        :return: Food in json
        """
        headers = {
            'X-Yummly-App-ID': self.api_id,
            'X-Yummly-App-Key': self.api_key,
        }

        result = requests.get(URL_SINGLE + id , headers=headers)
        return result

    def getMeta(self, key):
        """
        Get names of metadata by key
        :param key: The name of the metadata
        :return: metadata
        """
        headers = {
            'X-Yummly-App-ID': self.api_id,
            'X-Yummly-App-Key': self.api_key,
        }

        result = requests.get(URL_METADATA + key , headers=headers)
        return result

def post(url, data, password):
    """
    Make POST request. This function is used for synchronisation of Flask server and local files
    :param url: URL for request
    :param data: data for request
    :param password: user's password for server - the same like password for instagram
    :return: Request response
    """
    result = None
    headers = { 'password' : password }

    # try because the server may be down
    try:
        result = requests.post(url,json=data, headers=headers )
        return result
    except:
        pass

