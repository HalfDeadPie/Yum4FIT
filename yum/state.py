import yum.Parser as Parser
import yum.CONSTANTS as CONST
from yum import cli

class State:
    """
    Represents the actual state of the user
    """
    def __init__(self, likes, save):
        """
        Constructor of the state
        :param likes: count of likes on Yum4FIT foods
        :param save: True or False if just creating empty state
        """
        self.likes = likes
        self.xp = likes * CONST.XP_FACTOR
        self.level = int(self.xp / 10)
        if(save):
            self.save()
        else:
            self.load()

    def likes(self, value):
        """
        Function that save state depending on likes
        :param value: The count of likes
        """
        self.likes = value
        self.xp = value * CONST.XP_FACTOR
        self.level = self.xp % 10
        self.save()

    def save(self):
        """
        Saving the game - writing the state to file savegame.cfg
        """
        fields = [ 'level' , 'xp', 'likes' ]
        values = [ str(self.level), str(self.xp), str(self.likes) ]
        Parser.updateSave(CONST.SAVE_FILE, 'save', fields, values)


    def load(self):
        """
        Loading the state from savegame.cfg file
        :return:
        """

        # check the state file here
        if not Parser.exists(CONST.SAVE_FILE):
            self.initState()

        self.likes = int( Parser.get(CONST.SAVE_FILE, 'save', 'likes') )
        self.xp = int( Parser.get(CONST.SAVE_FILE, 'save', 'xp') )
        self.level = int( Parser.get(CONST.SAVE_FILE, 'save', 'level') )
        return self

    def initState(self):
        fields = [ 'level' , 'xp', 'likes' ]
        values = [ '0', '0', '0' ]
        Parser.updateSave(CONST.SAVE_FILE, 'save', fields, values)


    def text(self):
        """
        Simple representation of state
        :return: State in text
        """
        result = ''
        result += 'Level: ' + str(self.level)
        result += '\nXP: ' + str(self.xp)
        result += '\nLikes: ' + str(self.likes)
        need = (10 * (self.level + 1)) - self.xp
        result += '\nYou need ' + str(need) + ' XP for next level\n'
        return result

