from InstagramAPI import InstagramAPI

class Guest:
    """
    Represents Guest, who agreed with eating together with host
    """
    def __init__(self, username, password):
        """
        Constructor of the guest, who logged to instagram via Flask server
        :param username: Instagram username
        :param password: Instagram password
        """
        self.username =  username
        self.password = password
        self.ig = InstagramAPI(username, password)

    def login(self):
        """
        Guest login
        :return: True or None
        """
        return self.ig.login()

    def logout(self):
        """
        Guest logout
        :return: True or None
        """
        return self.ig.logout()

    def yum(self, id):
        """
        Represents like and agreeing with eating together with host
        :param id: ID of the food
        :return: True or False if error
        """
        self.ig.like(id)
