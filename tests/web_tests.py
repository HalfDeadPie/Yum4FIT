from yum import web

def test_create_app():
    """Test the app creating and its name"""
    app = web.YumWeb(__name__)
    assert app.name == 'web_tests'