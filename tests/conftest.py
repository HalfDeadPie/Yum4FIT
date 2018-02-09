import json
import os
import string
from random import choice

from flexmock import flexmock


ABS_PATH = os.path.abspath(os.path.dirname(__file__))
FIXTURES_PATH = ABS_PATH + '/fixtures/'
CONFIGS_PATH = FIXTURES_PATH + 'config/'
DATA_PATH = FIXTURES_PATH + '/data'

HASHTAG = '#Yum4FIT'

FOOD_NAME = "Spiced Pumpkin Mix"
FOOD_URL = "http://bsinthekitchen.com/spiced-pumpkin-mix/"
FOOD_INGREDIENTS = "1 can (400 ml or 1½ cups) pureed pumpkin,1 tablespoon pumpkin pie spice,½ cup sugar,2 tbsp vanilla extract"
FOOD_PICTURE = "https://lh3.googleusercontent.com/zMcDOVjlmAGfSNMWJPwwRs0TxsEb6mXx3ZbaPTZ3AmEa_3_p1TKT4dALk2A2Mku9dtHGoidGlbKs2Usy5uJ6Xg=s360"

PERSON_FULLNAME = "John Doe"
PERSON_EMAIL = "yumhalfdead@gmail.com"
PERSON_USERNAME = 'yumhalfdead'
PERSON_PASSWROD = 'BlackSabbath123'

REAL_CONFIG = 'config.cfg'

RANDOM_STRING = "kjojfniasjfnias"

TESTING_CAPTION = 'This caption is only testing caption #testing'

FAKE_CTX = flexmock(obj = {
                            'config': 'fuck.cfg' },
                    resilient_parsing = False,
                    exit=lambda: None)

ERROR_MSG_CONFIG = "Something is wrong with the configuration file\n"

SERVER_URL = "http://127.0.0.1:5000/"

class invoker():

    @staticmethod
    def testingServer():
        return SERVER_URL

    @staticmethod
    def testingUsername():
        return os.environ['TEST_USERNAME']

    @staticmethod
    def testingPassword():
        return os.environ['TEST_PASSWORD']

    @staticmethod
    def errMsgConfig():
        return ERROR_MSG_CONFIG

    @staticmethod
    def caption():
        return TESTING_CAPTION

    @staticmethod
    def fake_ctx():
        return FAKE_CTX

    @staticmethod
    def randomString():
        return RANDOM_STRING

    @staticmethod
    def personFullname():
        return PERSON_FULLNAME
    @staticmethod
    def personEmail():
        return PERSON_EMAIL

    @staticmethod
    def personUsername():
        return PERSON_USERNAME

    @staticmethod
    def personPassword():
        return PERSON_PASSWROD

    @staticmethod
    def load_data(name):
        with open(DATA_PATH + '/' + name + '.json') as f:
            return f.read()

    @staticmethod
    def getDataPath(name):
        return DATA_PATH + "/" + name

    @staticmethod
    def hashtag():
        return HASHTAG

    @staticmethod
    def configs():
        return CONFIGS_PATH

    @staticmethod
    def real_config():
        return REAL_CONFIG

    @staticmethod
    def foodName():
        return FOOD_NAME

    @staticmethod
    def foodIngredients():
        return FOOD_INGREDIENTS

    @staticmethod
    def foodPicture():
        return FOOD_PICTURE

    @staticmethod
    def foodURL():
        return FOOD_URL

