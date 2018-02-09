"""
The user should set theese paths according to operation system, but the names of the files should stay the same
"""
import os

WD = os.path.dirname(os.path.abspath(__file__))

# file for saving of user's status
SAVE_FILE = WD + '/savegame.cfg'

# file for saving user's last recipe
RECIPE_FILE = WD + '/recipe.cfg'

# file for saving relations between friends and food
# Hint: if you eat with friend, add him and his like will provide you more XP
FRIENDS_FILE = WD + '/friends.cfg'

# path to GUI main window
WINDOW = WD + '/mainwindow.ui'

# summary of all likes on your food * XP_FACTOR = XP
XP_FACTOR = 5

# the maximal result of founded food
MAX_RESULTS = 5

