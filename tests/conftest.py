import pytest
from app.main import app
from app.database import init_db, close_db

@pytest.fixture
def client():
    """Test client for the Flask application."""
    init_db()

    with app.test_client() as client:
        yield client

    close_db()
