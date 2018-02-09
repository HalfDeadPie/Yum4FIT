import json
import urllib
import webbrowser

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QListView, QListWidgetItem, QListWidget, QGroupBox, QTextBrowser, \
    QCheckBox, QFileDialog, QInputDialog, QLineEdit
from PyQt5.uic.Compiler.qtproxies import QtWidgets
from PyQt5 import QtWidgets, uic, QtGui

from yum import CONSTANTS, Parser, account, state, food, yum, connector


class GUI():
    """
    Class representing and provides Yum4FIT services via graphic user interface. To open the GUI
    run "yum run" command
    """
    def __init__(self, config):
        """
        Constructor of the GUI class
        :param config: Config file (default=config.cfg)
        """
        app = QtWidgets.QApplication([])
        window = QtWidgets.QMainWindow()
        window.setWindowTitle("Yum4FIT")
        with open(CONSTANTS.WINDOW) as f:
            uic.loadUi(f, window)
        self.app = app
        self.w = window
        self.config = config
        self.profile = None
        self.state = None
        self.password = None
        self.hashtag = None

        self.show()

    def show(self):
        """
        Function to set all the elements and show the main window
        :return: running configured GUI application
        """
        self.login()

        self.loadProfileBox()

        self.loadFood()

        self.loadRecipe()

        self.loadShareButton()

        self.loadFriendButton()

        self.w.show()
        return self.app.exec()

    def login(self):
        """
        Login to Instagram
        """
        username = Parser.getUsername(None, self.config)
        password = Parser.getPassword(None, self.config)
        account.login(username, password)
        self.profile = account.getProfile()
        self.password = password
        self.hashtag = Parser.get(self.config,'instagram', 'hashtag')

    # ------------------------------------------------------------------------------------------------------------------

    def loadUsername(self):
        """
        Load username to label in profile block
        :return:
        """
        label = self.w.findChild(QtWidgets.QLabel, 'labUsername')
        label.setText(self.profile.username)
        label.setAlignment(Qt.AlignCenter)

    def loadFullname(self):
        """
        Load full name  to label in profile block
        """
        label = self.w.findChild(QtWidgets.QLabel, 'labFullname')
        label.setText(self.profile.full_name)
        label.setAlignment(Qt.AlignCenter)

    def loadEmail(self):
        """
        Load email to label in profile block
        """
        label = self.w.findChild(QtWidgets.QLabel,'labEmail')
        label.setText(self.profile.email)
        label.setAlignment(Qt.AlignCenter)

    def loadPicture(self):
        """
        Load picture of user to label in profile block
        """
        url = self.profile.avatar
        data = urllib.request.urlopen(url).read()

        image = QtGui.QImage()
        image.loadFromData(data)

        lbl = self.w.findChild(QtWidgets.QLabel,'labPicture')
        lbl.setPixmap(QtGui.QPixmap(image))
        lbl.setAlignment(Qt.AlignCenter)

    def loadState(self):
        """
        Load state of the user and set the level in profile block
        :return:
        """
        self.state = state.State(0, False)
        label = self.w.findChild(QtWidgets.QLabel,'labLevel')
        label.setAlignment(Qt.AlignCenter)
        label.setText("Level: " + str(self.state.level))

    def loadGainButton(self):
        """
        Set the gain button
        """
        button = self.w.findChild(QtWidgets.QPushButton, 'buttonGain')
        button.setText("Gain")
        button.clicked.connect(self.gain)

    def loadProfileBox(self):
        """
        Load profile box
        :return:
        """
        self.loadUsername()
        self.loadFullname()
        self.loadEmail()
        self.loadPicture()
        self.loadState()
        self.loadGainButton()

    # ------------------------------------------------------------------------------------------------------------------

    def loadFood(self):
        """
        Load all the user's food from instagram - depending on Yum4FIT hashtag
        """
        self.foods = account.getAllFood(self.profile.username, self.password, self.hashtag)
        listView = self.w.findChild(QtWidgets.QListWidget, 'listFoods')
        listView.setViewMode(QListView.IconMode)
        listView.setIconSize(QSize(400, 400))
        listView.clear()

        for actual in self.foods:
            f = actual.split(' ')

            url = f[1]
            data = urllib.request.urlopen(url).read()
            image = QtGui.QImage()
            image.loadFromData(data)
            map = QtGui.QPixmap(image)

            item = QListWidgetItem(f[0])
            icon = QtGui.QIcon()
            icon.addPixmap(map,QtGui.QIcon.Normal, QtGui.QIcon.Off)
            item.setIcon(icon)
            listView.addItem(item)

    # ------------------------------------------------------------------------------------------------------------------

    def loadRecipe(self):
        """
        Load last food from recipe file
        """
        self.lastFood = food.Food(None)
        self.lastFood = self.lastFood.load(CONSTANTS.RECIPE_FILE)

        self.loadActualName()
        self.loadIngredients()
        self.loadActualImage()

        self.loadGenerateButton()
        self.loadGuideButton()

    def reloadRecipe(self):
        """
        Refresh the last food
        """
        self.lastFood = food.Food(None)
        self.lastFood = self.lastFood.load(CONSTANTS.RECIPE_FILE)

        self.loadActualName()
        self.loadIngredients()
        self.loadActualImage()

    def loadActualName(self):
        """
        Load actual name of the food to group box
        """
        box = self.w.findChild(QtWidgets.QGroupBox, 'boxActual')
        box.setTitle(self.lastFood.name)

    def loadIngredients(self):
        """
        Load ingredients of the last recipe to the group box of last food
        :return:
        """
        text = self.w.findChild(QtWidgets.QTextBrowser, 'textIngredients')
        text.setText(self.lastFood.ingredients)

    def loadActualImage(self):
        """
        Load the actual image of last food from recipe file to last food group box
        :return:
        """
        url = self.lastFood.picture
        data = urllib.request.urlopen(url).read()

        image = QtGui.QImage()
        image.loadFromData(data)

        map = QtGui.QPixmap(image)

        imageLabel = self.w.findChild(QtWidgets.QLabel, 'actualImage')
        imageLabel.setPixmap(map.scaledToWidth(200))
        imageLabel.setAlignment(Qt.AlignCenter)

    def loadGenerateButton(self):
        """
        Set generate button - generates new recipes. User is able to set parameters of searching to config file
        and set the checkbox to use theese parameters.
        :return:
        """
        button = self.w.findChild(QtWidgets.QPushButton, 'buttonGenerate')
        button.setText("Generate")
        button.clicked.connect(self.recipe)

    def loadGuideButton(self):
        """
        Set guide step-by-step button. This button opens the browser and redirect to URL of food.
        :return:
        """
        button = self.w.findChild(QtWidgets.QPushButton, 'buttonGuide')
        button.setText("Guide")
        button.clicked.connect(self.redirect)

    # ------------------------------------------------------------------------------------------------------------------

    def loadShareButton(self):
        """
        Set buton for sharing food
        :return:
        """
        button = self.w.findChild(QtWidgets.QPushButton, 'buttonShare')
        button.setText("Share")
        button.clicked.connect(self.share)

    def loadFriendButton(self):
        """
        Set button for adding friend. The username writes to line friend's Instagram username and click on the food in
        the list. Then click on this button
        """
        button = self.w.findChild(QtWidgets.QPushButton, 'buttonFriend')
        button.setText("Add friend")
        button.clicked.connect(self.addFriend)

    # ------------------------------------------------------------------------------------------------------------------

    def gain(self):
        """
        Support function to gain XP from likes
        """
        state = account.gain(self.profile.username, self.password, self.hashtag, None, CONSTANTS.FRIENDS_FILE)
        data = { 'likes' : str(state.likes),
                 'level' : str(state.level),
                 'xp' : str(state.xp )
                 }
        json_data = json.dumps(data)
        url = Parser.get(self.config, 'server', 'url')
        url += 'gain'
        connector.post(url, json_data, self.password)
        self.loadState()

    def redirect(self):
        """
        Support function to open browser and redirect
        """
        new = 2
        url = self.lastFood.url
        webbrowser.open(url, new=new)

    def recipe(self):
        """
        Support function to generate recipe
        """
        api_id = Parser.get(self.config, 'yummly', 'api-id')
        api_key = Parser.get(self.config, 'yummly', 'api-key')
        server_url = Parser.get(self.config, 'server', 'url')
        yummer = yum.Yum(api_id, api_key, server_url)

        checkbox = self.w.findChild(QtWidgets.QCheckBox, 'checkConfig')
        file = False
        if checkbox.isChecked():
            file = True

        print("choosing recipe...")
        result = yummer.recipe(diet=None, allergy=None,
                            cuisine=None, exclude_cuisine=None,
                            ingredient=None, exclude_ingredient=None,
                            holiday=None, exclude_holiday=None,
                            phrase=None,
                            file=file, config=self.config)
        if result:
            print("reloading...")
            self.reloadRecipe()

    def share(self):
        """
        Support function for sharing photos of the food. Includes opening file dialog and setting caption
        :return:
        """
        file = self.open()
        if file != None:
            caption = self.setCaption()
            if caption == None:
                caption = ""
            hashtag = Parser.get(self.config, 'instagram', 'hashtag')
            server_url = Parser.get(self.config, 'server', 'url')
            account.upload(self.profile.username, self.password, file, caption +" "+ hashtag, server_url)
            self.loadFood()

    def open(self):
        """
        Support function to open file dialog with filter of jpeg files
        """
        fileName, _ = QFileDialog.getOpenFileName(caption="Choose image for uploading to Instagram",
                                                  directory="",filter="Images (*.jpeg, *.jpg)")
        if fileName:
            return fileName

    def setCaption(self):
        """
        Open special input dialog for setting the caption
        :return:
        """
        text, okPressed = QInputDialog.getText(None,"Enther the captiong of image","Caption:", QLineEdit.Normal, "")
        if okPressed and text != '':
            return text

    def addFriend(self):
        """
        Support function to add friend using the item chosen by clicking to listWidget of foods
        """
        line = self.w.findChild(QtWidgets.QLineEdit, 'lineFriend')
        friend = line.text()

        if(friend == None or friend == ""):
            return
        else:
            listView = self.w.findChild(QtWidgets.QListWidget, 'listFoods')
            id = listView.currentItem().text()
            if id:
                data = {"username": friend, "post": id}
                json_data = json.dumps(data)
                url = Parser.get(self.config,'server','url')
                url += 'addfriend'
                Parser.updateSection(CONSTANTS.FRIENDS_FILE, friend, id, 'no')
                connector.post(url, json_data, self.password)