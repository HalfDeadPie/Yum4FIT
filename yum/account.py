from InstagramAPI import InstagramAPI

import yum.state as state
from yum import Parser, CONSTANTS, connector
from yum.profile import Profile
import sys

ig = InstagramAPI
def login(username, password):
    """
    Login to Instagram
    :param username: user's login
    :param password: user's password
    :return: True - sucessful, False - unsucessful
    """
    global ig
    ig = InstagramAPI(username, password)
    if(ig.isLoggedIn == False):
        result = ig.login()
        if(result == None):
            sys.exit('Wrong creddentials for Instagram!')
        return result
    else:
        return True

def logout():
    """
    Logout from Instagram
    """
    if(hasattr(ig, "isLoggedIn") and ig.isLoggedIn):
        ig.logout()
        ig.isLoggedIn = False

def upload(username, password, path, caption, url):
    """
    Upload photo to Instagram
    :param username: Instagram username
    :param password: Instagram password
    :param path:  Path to picture
    :param caption: Caption enriched with hashtag
    :return:
    """
    login(username, password)
    ig.uploadPhoto(path, caption)
    print('Uploading finished.')
    connector.post(url + 'reload', "", password)

def getAllMedias(username, password):
    """
    Get all your medias from Instagram account
    :param username: Instagram login
    :param password: Instagram password
    :return: All your Instagram Posts
    """
    login(username, password)

    import time
    myposts = []
    has_more_posts = True
    max_id = ""
    while has_more_posts:
        ig.getSelfUserFeed(maxid=max_id)
        if ig.LastJson['more_available'] is not True:
            has_more_posts = False  # stop condition

        max_id = ig.LastJson.get('next_max_id', '')
        myposts.extend(ig.LastJson['items'])  # merge lists
        time.sleep(2)  # Slows the script down to avoid flooding the servers

    return myposts

def getAllFood(username, password, hashtag):
    """
    Get all your Yum4FIT food from Instagram
    :param username: Instagram Login
    :param password: Instagram Password
    :param hashtag: Special Yum4FIT Hastag (default #Yum4FIT
    :return: All ID with URLs as string
    """
    result = []
    allMedia = getAllMedias(username, password)
    for actual in allMedia:
        if (actual['caption'] != None):
            if hashtag in actual['caption']['text']:
                id = actual['id']
                url = actual['image_versions2']['candidates'][0]['url']
                result.append(id + " " + url)
    return result

def sumLikes(allMedia, hashtag, friendsFile):
    """
    Summary of all likes on Yum4FIT posts
    :param allMedia: All your Instagram posts
    :param hashtag: The specific hashtag for Yum4FIT
    :return: The summary of all likes on Yum4FIT posts
    """
    summary = 0
    # all together
    #print(json.dumps(allMedia))
    for post in allMedia:
        if(post['caption'] != None):
            if (hashtag in post['caption']['text']):
                likes_count = post['like_count']
                id = post['id']
                for liker in post['likers']:
                    usr = liker['username']
                    agreed = Parser.get(friendsFile, usr, id)
                    if agreed=='yes':
                        likes_count += 4
                summary += int(likes_count)
    user = state.State(summary,True)
    return user


def gainFromId(allMedia, hashtag, id):
    """
    Print XP Gain from one post
    :param allMedia: All your Instagram posts
    :param hashtag: Specific hashtag for Yum4FIT
    :param id: ID of the media
    :return: XP Gain
    """
    summary = 0
    for post in allMedia:
        if (post['caption'] != None and post['id'] == id):
            if (hashtag in post['caption']['text']):
                likes_count = post['like_count']
                summary += int(likes_count)
    return summary

def gain(username, password, hashtag, id, friendsFile):
    """
    Calculate the XP Gain from all Instagram posts of Yum4FIT foods
    :param username: Instagram Login
    :param password: Instagram Password
    :param hashtag: Specific hashtag for Yum4FIT
    :param id: ID of the instagram media
    :return: XP Gain
    """
    allMedia = getAllMedias(username, password)
    if(id == None):
        return sumLikes(allMedia, hashtag, friendsFile)
    else:
        return gainFromId(allMedia, hashtag, id)

def getProfile():
    """
    Get the profile from instagram
    :return: User's profile
    """
    if(ig.isLoggedIn):
        ig.getProfileData()
        response = ig.LastJson
        username = response['user']['username']
        fullName = response['user']['full_name']
        email = response['user']['email']
        avatar = response['user']['profile_pic_url']
        profile = Profile(username, fullName, email, avatar)
        return profile

def yum(id):
    if(ig.isLoggedIn):
        ig.like(id)
