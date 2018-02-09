import json
import flask
import os
import yum.account as acc
import yum.CONSTANTS as CONST

from yum import Parser, food, state
from yum.Guest import Guest
from .cli import cli
from click._unicodefun import click
from flask import request

class YumWeb(flask.Flask):
    """
    Represents web part of the application - Flask server
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor of the flask server
        """
        super().__init__(*args, **kwargs)

app = YumWeb(__name__)
@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Index page
    Check the metod and call method processing
    """
    method = request.method
    if method == 'GET':
        return processGet()

@app.route('/login', methods=['POST'])
def processGuestLogin():
    """
    Process guest login and sending the yum
    Yum is representation of like and agreeing with sharing food with host
    :return: redirection back
    """
    method = request.method
    if (method == 'POST'):
        username = request.form['username']
        password = request.form['password']
        foods = request.form.getlist("food")

        if(username != None and
           password != None and
           len(foods) != 0):
            # login and like
            yumFood(username, password, foods)

            # update food in friends list to yes
            for id in foods:
                if Parser.has_field(app.friends_file, username.lower(), id):
                    Parser.updateSection(app.friends_file, username.lower(), id, 'yes')

        return flask.redirect('/',302)

@app.route('/addfriend', methods=['POST'])
def addRemoteFriend():
    """
    Processing POST method from local for adding friend on the server side
    :return: Code 200 if ok
    """
    method = request.method
    if(method == "POST" and checkPassword(request, app.admin_password)):
        j = json.loads(request.json)
        username = j['username']
        postID = j['post']
        Parser.updateSection(app.friends_file, username, postID, 'no')
    return "200"

@app.route('/gain', methods=['POST'])
def gain():
    """
    Processing POST method from local for gaining XP points on the server side
    :return:
    """
    method = request.method
    fields = [ 'level' , 'xp', 'likes' ]
    values = []
    if(method == "POST" and checkPassword(request, app.admin_password)):
        j = json.loads(request.json)
        for f in fields:
            values.append(j[f])
        Parser.updateSave(app.save_file, 'save', fields, values)
    return "200"

@app.route('/saverecipe', methods=['POST'])
def saveRecipe():
    """
    Processing POST method from local for saving the new generated recipe
    :return:
    """
    method = request.method
    if(method == "POST" and checkPassword(request, app.admin_password)):
        j = json.loads(request.json)
        fields = ['name','url', 'ingredients','picture']
        values = []
        for f in fields:
            values.append(j[f])
        Parser.updateSave(app.recipe_file, 'recipe', fields, values)

    return "200"

@app.route('/reload', methods=['POST'])
def reload():
    """
    Reload the food list is the main purpose
    """
    method = request.method
    if(method == "POST" and checkPassword(request, app.admin_password)):
        reload(app)

    return "200"

@app.route('/confirmated', methods=['POST'])
def confirmated():
    """
    Send back to client confirmated friends
    :return: Confirmated friends
    """
    method = request.method
    if(method == "POST" and checkPassword(request, app.admin_password)):
        return getConfirmated(app.config)



@cli.command()
@click.pass_context
@click.option('--host', '-h', default="127.0.0.1")
@click.option('--port', '-p', default=5000)
@click.option('--debug', '-d', is_flag=True)
def run_server(ctx, host, port, debug):
    reload(app)
    app.run(host,port,debug)

def reload(app):
    """
    Reload the application data
    :param app: target application
    :return: reloaded application
    """
    print("reloading app...")
    config = setConfigFile()
    app.admin_username = Parser.getUsername(None, config)
    app.admin_password = Parser.getPassword(None, config)
    app.admin_hashtag = Parser.get(config, 'instagram', 'hashtag')
    app.admin_config = config
    app.recipe_file = CONST.RECIPE_FILE
    app.friends_file = CONST.FRIENDS_FILE
    app.save_file = CONST.SAVE_FILE
    app.food_list = acc.getAllFood(app.admin_username, app.admin_password, app.admin_hashtag)
    app.profile = acc.getProfile()

def setConfigFile():
    """
    Set configuration file - check the YUM_CONFIG in environment variables
    :return: config filepath
    """
    if "YUM_CONFIG" in os.environ:
        return os.environ['YUM_CONFIG']
    else:
        return 'config.cfg'

def processGet():
    """
    Support function to process GET method on the index side. Loads the food and render index page
    :return: rendering the index page
    """
    posts = []
    for food in app.food_list:
        posts.append(food.split(' '))

    lastFood = loadLastRecipe()
    user = state.State(0,False)
    ingredients = lastFood.ingredients
    return flask.render_template('index.html',
                                 posts=posts,
                                 profile = app.profile,
                                 last=lastFood,
                                 user=user,
                                 ingredients=ingredients)

def loadLastRecipe():
    """
    Loads last recipe from recipe.cfg file
    :return: last food of the user
    """
    lastFood = food.Food(None)
    lastFood = lastFood.load(app.recipe_file)
    return lastFood

def yumFood(username, password, foodList):
    """
    Yums the host's food by the guest user
    :param username: guest Instagram username
    :param password: guest Instagram password
    :param foodList: all yummed food on the index page
    """
    guest = Guest(username, password)
    result = guest.login()
    if result != None:
        for food in foodList:
            guest.yum(food)
        guest.logout()

def checkPassword(request, password):
    """
    Simple password-based authentication - the same password of the host like on the Instagram
    :param request: request to autheticate
    :param password: Instagram and Web password of the host user
    :return: True or False if authentication failed
    """
    if 'password' in request.headers:
        if password == request.headers['password']:
            print("PASSWORD OK")
            return True

    print("wrong password")
    return False

def getConfirmated(config):
    friends = Parser.getConfirmated(CONST.FRIENDS_FILE)
    return produceJson(friends)

def produceJson(confirmated):
    friends = []
    foods = []

    for line in confirmated:
        word = line.split(" ")
        friends.append(word[0])
        foods.append(word[1])

    json = buildJson(friends, foods)
    return json

def buildJson(fields, values):
    """
    Builds json
    :param fields: fields for json
    :param values: values for fields in json
    :return: json
    """
    i = 0
    data = {}
    for field in fields:
        data[field+'--'+values[i]] = values[i]
        i += 1

    json_data = json.dumps(data)
    return json_data