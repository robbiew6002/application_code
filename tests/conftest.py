import pytest
from app import create_app
from flask_bcrypt import Bcrypt


@pytest.fixture()
def app():
    app=create_app()
    app.config.update({
        "Testing": True
    })

    yield app

@pytest.fixture()
def bcrypt(app):
    return Bcrypt(app)

@pytest.fixture(scope='function')
def client(app):
    return app.test_client()
