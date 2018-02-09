Web part
======================

The web part of the application is builded using Flask. Flask server renders simple web page index that display brief information about
the host user. There is the profile box including information about the user on the top of the page. The actual/last food is displayed
right below the profile box. It consits of the name of the food, ingredients, step-by-step guide link and the picture of the food.

The third main part of the web is food list of the host user. Guest user is able to choose foods and give them *Yum*. Yum means like on the post
on the Instagram and also the confirmation of sharing that food with the host. So when host cooks the food, uploads it on Instagram and
set the guest as a *friend*, it should represents sharing of the food. After that, if the guests send *Yum* on the shared food, he confirms
that he shared the food and liked that! This is the main reason, why are for theese special likes more important that regular. Someone,
who really enjoyed your food appreciate your work.

Synchronisation of the data is achieved using POST method from GUI and CLI part to web. The web part uses mechanisms for authenticating and
processing theese requests.

Server may be started using CLI command `yum run_server`.