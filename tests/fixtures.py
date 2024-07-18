import pytest

from app import create_app
from app.core import db as SQLdb


@pytest.fixture
def client():
    """Create a test client using the app instance."""
    app = create_app("test")
    with app.app_context():
        with app.test_client() as client:
            yield client


@pytest.fixture
def db():
    yield SQLdb
    SQLdb.drop_all()
    SQLdb.session.remove()
