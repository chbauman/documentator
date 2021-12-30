import json
from pathlib import Path

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_app.database import Base
from main import app, get_db

# Paths
TEST_DIR = Path(__file__).parent
PROJECT_DIR = TEST_DIR.parent
TEST_DATA_DIR = TEST_DIR / "data"
TEST_IMG_PATH = TEST_DATA_DIR / "Entwurf.jpg"
TEMP_DIR = TEST_DIR / "temp"

# Remove test database if it exists
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
SQL_TEST_DB_PATH = Path("test.db")
if SQL_TEST_DB_PATH.exists():
    SQL_TEST_DB_PATH.unlink()

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

DEFAULT_CLIENT = TestClient(app)

test_user = {"email": "emailtest@fastapi.ch", "password": "lol_this_sucks"}
test_item = {
    "text": "this is a text intended for testing",
    "date_time": "2021-12-29T19:07:46.087Z",
}


def create_test_user(client: TestClient = None):
    """Create a user for testing."""
    if client is None:
        client = DEFAULT_CLIENT

    res = client.post("/users/", json.dumps(test_user))
    assert (
        res.status_code == 200
    ), f"Creating user failed: {res.status_code}, {res.text}"
    return res.json()


def create_user_item(user_id: int, client: TestClient = None):
    """Creates an item for a user."""
    if client is None:
        client = DEFAULT_CLIENT

    response = client.post(f"/users/{user_id}/items/", json.dumps(test_item))
    assert (
        response.status_code == 200
    ), f"Creating user item failed: {response.status_code}, {response.text}"
    return response.json()


def get_first_user_id():
    response = DEFAULT_CLIENT.get("/users/")
    assert response.status_code == 200
    first_user = response.json()[0]
    return first_user["id"]


def get_users_first_item(user_id: int):
    response = DEFAULT_CLIENT.get(f"/users/{user_id}/")
    assert response.status_code == 200
    all_items = response.json()["items"]
    assert len(all_items) > 0, f"{all_items}"
    return all_items[0]["id"]
