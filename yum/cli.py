import click
import yum.Parser as Parser
import yum.account as acc
import yum.state as state
import yum.yum as yum

from yum import connector, gui
from flask import json
import yum.CONSTANTS as CONST

@click.group('yum')
@click.option('--config', '-c', default='config.cfg',
              help='Path of the auth config file.')
@click.option('--username', '-u', envvar='IG_USERNAME',
              help='Instagram username')
@click.option('--password', '-p', envvar='IG_PASSWORD',
              help='Instagram password')
@click.pass_context
def cli(ctx, config, username, password):
    ctx.obj['config'] = config
    ctx.obj['username'] = username
    ctx.obj['password'] = password
    ctx.obj['recipe_file'] = CONST.RECIPE_FILE
    ctx.obj['save_file'] = CONST.SAVE_FILE
    ctx.obj['friends_file'] = CONST.FRIENDS_FILE
    ctx.obj['server_url'] = Parser.get(config,'server','url')

@cli.command()
@click.pass_context
@click.option('--caption', '-c', default='Check my Yum4FIT food!',
              help='Caption for Instagram picture')
@click.argument('path')
def share(ctx, path, caption):
    """
    Share photo on instagram
    :param path: Path to the picture
    :param caption: Caption of picture on instagram
    """
    config = ctx.obj['config']
    username = Parser.getUsername(ctx.obj['username'], config)
    password = Parser.getPassword(ctx.obj['password'], config)
    hashtag = Parser.get(config, 'instagram', 'hashtag')
    serverURL = ctx.obj['server_url']
    acc.upload(username, password, path, caption +" "+ hashtag, serverURL)

@cli.command()
@click.option('--id', '-i', help='XP Gain from the photo with ID')
@click.pass_context
def gain(ctx, id):
    """
    Gain XP from Yum4FIT pictures on Instagram
    :param id: Returns the XP gain only from the picture with the ID set as an argument
    :return: XP Gain
    """
    config = ctx.obj['config']
    username = Parser.getUsername(ctx.obj['username'], config)
    password = Parser.getPassword(ctx.obj['password'], config)
    hashtag = Parser.get(config, 'instagram', 'hashtag')
    friendsFile = ctx.obj['friends_file']
    serverURL = ctx.obj['server_url']

    setConfirmed(password, serverURL)

    result = acc.gain(username, password, hashtag, id, friendsFile)

    if not id:
        data = { 'likes' : str(result.likes),
                 'level' : str(result.level),
                 'xp' : str(result.xp )
                 }
        json_data = json.dumps(data)
        url = ctx.obj['server_url']
        url += 'gain'
        connector.post(url, json_data, password)

    # result is state
    if(id == None):
        click.echo( result.text() )
    # result is likes count
    else:
        click.echo("%s: " % id + "%d likes" % result + " (%s XP)" % (result * CONST.XP_FACTOR))

@cli.command()
@click.pass_context
def food(ctx):
    """
    Print all the Yum4FIT food on your instagram
    :param ctx:
    :return:
    """
    config = ctx.obj['config']
    username = Parser.getUsername(ctx.obj['username'], config)
    password = Parser.getPassword(ctx.obj['password'], config)
    hashtag = Parser.get(config, 'instagram', 'hashtag')
    food = acc.getAllFood(username, password, hashtag)
    for actual in food:
        print(actual)

@cli.command()
@click.pass_context
@click.argument('username')
@click.argument('id')
def add_friend(ctx, username, id):
    data = {"username": username, "post": id}
    json_data = json.dumps(data)
    url = ctx.obj['server_url']
    url += 'addfriend'
    Parser.updateSection(CONST.FRIENDS_FILE, username, id, 'no')
    config = ctx.obj['config']
    password = Parser.getPassword(ctx.obj['password'], config)
    connector.post(url, json_data, password)

@cli.command()
@click.pass_context
@click.option('--diet', '-d', help='The diet-allowed recipe. Supported diets are lacto vegatarian, '
                                   'ovo vegetarian, pescetarian, vegan and lacto-ovo vegetarian')
@click.option('--ingredient', '-i', help='Find the recipe with the ingredient')
@click.option('--allergy', '-a', help='The allergy-allowed recipe. Supported allergies are dairy, egg, gluten, peanut, seafood, sesame, soy, '
                                      'sulfite, tree nut and wheat')
@click.option('--cuisine', '-c', help='Allow the recipes from national cuisines. Supported cuisines are American, Italian, Asian, Mexican, '
                                      'Southern & Soul Food, French, Southwestern, Barbecue, Indian, Chinese, Cajun & Creole, English, '
                                      'Mediterranean, Greek, Spanish, German, Thai, Moroccan, Irish, Japanese, Cuban, Hawaiin, Swedish, '
                                      'Hungarian, Portugese')
@click.option('--holiday', '-h', help='Find the holiday recipes')
@click.option('--exclude-holiday', '-eh', help='Exclude the recipes from the holidays')
@click.option('--exclude-cuisine', '-ec', help='Exclude the recipes from national cuisines. Supported cuisines are the same like in --cuisine option')
@click.option('--exclude-ingredient', '-ei', help='Exclude the recipes from igredients. Supported cuisines are the same like in --cuisine option')
@click.option('--phrase', '-p', help='Find the recipe matching the phrase')
@click.option('--file','-f', is_flag=True)
def recipe(ctx, diet, allergy, cuisine, exclude_cuisine, ingredient, exclude_ingredient, holiday, exclude_holiday, phrase, file):
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
    """
    config = ctx.obj['config']
    api_id = Parser.get(config, 'yummly', 'api-id')
    api_key = Parser.get(config, 'yummly', 'api-key')
    server_url = Parser.get(config,'server','url')
    yummer = yum.Yum(api_id, api_key, server_url)
    result = yummer.recipe(diet, allergy,
                           cuisine, exclude_cuisine,
                           ingredient, exclude_ingredient,
                           holiday, exclude_holiday,
                           phrase,
                           file, config)
    if result:
        print(result.text())

@cli.command()
@click.pass_context
def run(ctx):
    gui.GUI( ctx.obj['config'] )

def setConfirmed(password, url):
    response = connector.post(url+'confirmated', "", password)
    parser = Parser.parse(CONST.FRIENDS_FILE)
    friends = parser.sections()
    if not response:
        return
    data = json.loads(response.text)

    sections = []
    fields = []
    for local in friends:
        for new in data:
            extern = new.split('--')[0]
            if extern == local:
                sections.append(local)
                fields.append(data[new])

    for s in sections:
        for f in fields:
            Parser.updateSection(CONST.FRIENDS_FILE, s, f, 'yes')



if __name__ == '__main__':
    cli(obj={})
