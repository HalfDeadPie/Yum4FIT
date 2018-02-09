import os
import pytest

from conftest import invoker

from yum import account

@pytest.mark.parametrize(['username','password'],
                         [ ( invoker.testingUsername(), invoker.testingPassword() ),
                          ("randomUsername" , "badPassword") ])
def test_login(username, password):


    if password == 'badPassword':
        with pytest.raises(SystemExit):
            result = account.login(username, password)
            assert result == None
    else:
        result = account.login(username, password)
        assert  result == True

def test_share_and_list():
    caption = invoker.randomString()
    username = invoker.testingUsername()
    password = invoker.testingPassword()
    hashtag = invoker.hashtag()
    path = invoker.getDataPath('ramen.jpg')

    account.upload( username,
                    password,
                    path,
                    caption,
                    invoker.testingServer())

    result = account.getAllFood(username, password, hashtag)
    assert len(result) > 0

