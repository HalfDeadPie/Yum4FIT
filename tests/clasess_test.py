import pytest

from conftest import invoker
from yum.food import Food
from yum.profile import Profile


def test_foodLoader():
    data = Food(None)
    data.load(invoker.configs() + "/recipe.cfg")
    assert data.name == invoker.foodName()
    assert data.url == invoker.foodURL()
    assert data.picture == invoker.foodPicture()
    assert data.ingredients == invoker.foodIngredients()

def test_foodText():
    data = Food(None)
    data.load(invoker.configs() + "/recipe.cfg")
    output = data.text()
    assert invoker.foodName() in output
    assert 'Ingredients:' in output
    assert invoker.foodURL() in output

@pytest.mark.parametrize('full_name', [ invoker.personFullname(), None ])
def test_profile(full_name):
    if full_name:
        tester = Profile(invoker.personUsername(),
                full_name,
                invoker.personEmail(),
                "https://shirtoid.com/wp-content/uploads/2016/03/Zaphod-2016.jpg")
        assert tester.full_name == invoker.personFullname()

    else:
        tester = Profile(invoker.personUsername(),
                full_name,
                invoker.personEmail(),
                "https://shirtoid.com/wp-content/uploads/2016/03/Zaphod-2016.jpg")
        assert tester.full_name == "Anonymous"






