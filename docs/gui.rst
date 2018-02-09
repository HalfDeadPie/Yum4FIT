Graphic user interface
=============================

The main purpose of graphic user interface of this applications is to provide the functionality for users, who prefer GUI over CLI.
Interface is very simple and minimalistic. Here you can see example:

Example of user's GUI
#############################

.. image:: _static/gui.png
   :width: 900px
   :height: 900px
   :scale: 100 %
   :alt: alternate text
   :align: center

GUI parts
#################################

   - **Food list**

         As you can see on the example, *All your food* block shows the brief list of all user's food posts. Every item of this list
         consits of the picture of image (picture from Instagram) and the ID of that Instagram post. The main purpose of this
         was to extend the functionality of Instagram for this use. It's scrollable and its images are loaded from the URLs.

   - **Add friend button**

         Button *Add friend* under the list adds friend to friend list. The username of the friend must be written to input line next to button
         and one item(food) have to be chosen in the list.

   - **Share button**

         Button *Share* open filedialog, in which user may choose the picture. After that, the caption may be set. Click on this button
         includes uploading chosen picture to Instagram.

   - **Profile box**

         Profile block sumarizes brief information about the host user - username, fullname, email, profile picture and level. Profile box
         includes also *Gain button*

   - **Gain button**

         Click on this button runs collecting yums from the users - it means the likes on Instagram posts will be collected and the new
         state will be set. The level of the user may change after this action.

   - **Actual/last recipe box**

         The box under the profile displays the name and ingredients of the actual/last recipe. Mostly, there is also the picture of that food
         loaded from the URL. There are two special buttons inside this box.

   - **Guide button**

         *Guide button* opens the browser and redirects to the page, where should be step-by-step guide how to cood actual/last food and
         see more detail information about the food.

   - **Generate button**

         Generates the new recipe to the actual recipe box. If the user wants to set some searching parameters, all he needs to do is
         to write them to section *[parameters]* in configuration file. To load parameters from file, *Checkbox "Parameters from config file"*
         must be checked.


