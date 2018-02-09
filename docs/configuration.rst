Configuration
========================================

This part briefly talks about the configuration of Yum4FIT application. If the use wants to properly use the functionality
of this application, there is need to be some configuration done. The recommendation is to create **config.cfg** file,
which is called configuration file or config file.

Example of the config file::

    [instagram]
    username = RandomUser
    password = MyTotalySecretPassword
    hashtag = #Yum4FIT

    [yummly]
    api-id = Th1s1sTh31D
    api-key = 4ppl1c4t10nk3yfr0mYuMmlY

    [server]
    url = http://someserver:5000/


Section [instagram]
################################

    This section includes parameters for InstagramAPI.

    - username - Instagram username
    - password - Instagram password
    - hashtag - Instagram hashtag for #Yum4FIT food - not recommended to change

Section [yummly]
################################

    - api-id - Application identification code on Yummly
    - api-key - Application key code on Yummly

Section [server]
################################

    - url - URL of the deployed Flask server of the host user