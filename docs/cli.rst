Command line interface
==================================

The Yum4FIT provides command line interface. The commands are of this application are accessible via
entry point **yum**. It offers an option to set a few parameters via command line

Options
###################################

    - --config/-c - set the path and filename to configuration file
    - --username/-u - Instagram username in CLI part. May be set as environment variable
        *IG_USERNAME*
    - --password/p Instagram password used in CLI part. May be set as environment variable
        *IG_PASSWORD*

Commands
###################################

    - **recipe**

        Generates the level-respected recipe. This command returns the name of the food,
        needed ingredients and hyperlink to the step-by-step guide with details, how to cook the food.
        There are some parameters, that may be used with this command:

        - --diet/-d - filter foods according to diet
        - --alergy/-a - filter foods according to allergies
        - --cuisine/-c - filter foods according to national cuisines
        - --exclude_cuisine/-ec - filter foods according to excluded national cuisines
        - --ingredient/-i - filter foods according to ingredients
        - --exclude_ingredient/-ei - filter foods according to excluded ingredients
        - --holiday/-h - filter foods according to the holiday
        - --exclude_holiday/-eh - filter foods according to the excluded holiday
        - --phrase/-p - filter foods according to the phrase
        - --file/f - if this flag is set, CLI parameters are ignored and parameters and loaded
            from the configuration file in section *[parameters]*

    - **share**

        Uploads photo of the food on the Instagram. It needs the filepath as an argument.
        This command offers one option:

        - --caption/-c - caption for the Instagram post

    - **food**

        Provides the list of all user's Yum4FIT food *(with #Yum4FIT hashtag)* from Instagram. The food is represented
        with the *id* of the Instagram post and *url* of the Instagram photo

    - **gain**

        Collects the XP points calculated from the all sumarized likes of Yum4FIT posts. This command save the state and
        returns the simple text representation of the state. Using this command, user is able
        to achieve higher level. There is one option:

        - --id/-i - identification code of food post for retrieve XP gain from one post

    - **add_friend**

        Add friend to friend list with id of the food post. This commnad create relationship between the Instagram user
        and food, so it should represent cooking and sharing the food with friend. After this command, the friend is able
        to confirm sharing of the food via web part of application. The friend's like on the food has value of **5** regular
        likes. It needs two arguments - *username* of the friend and *id* of the food post.

    - **run_server**

        Runs the flask server, which is the web part of the application. There are some options:

        - --host/-h - server address
        - --port/-p - server port
        - --debug/-d - debug mode

    - **run**

        Opens the GUI part of the application
