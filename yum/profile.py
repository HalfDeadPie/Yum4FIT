class Profile:
    """
    Represents user's profile on the web
    """
    def __init__(self, username, full_name, email, avatar):
        """
        Constructor of web profile
        :param username: Instagram username
        :param full_name: Full name of the user - may be anonymous
        :param email: email of the user
        :param avatar: URL to the Instagram profile picture
        """
        self.username = username
        if full_name == None:
            self.full_name = "Anonymous"
        else:
            self.full_name = full_name
        self.email = email
        self.avatar = avatar
