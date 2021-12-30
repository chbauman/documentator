from fastapi.testclient import TestClient
from main import app
from test.util import (
    TEMP_DIR,
    TEST_IMG_PATH,
    create_test_user,
    create_user_item,
    get_first_user_id,
    get_users_first_item,
)

client = TestClient(app)


def test_create_user():
    created_user = create_test_user(client)
    created_user_id = created_user["id"]

    response = client.get("/users/")
    assert response.status_code == 200
    assert len(response.json()) == 1

    response = client.get(f"/users/{created_user_id}")
    assert response.status_code == 200


def test_create_user_item():
    user_id = get_first_user_id()

    create_user_item(user_id, client)

    response = client.get(f"/users/{user_id}/items/")
    assert response.status_code == 200, f"{type(user_id)} {response.json()}"
    assert len(response.json()) == 1


def test_file_upload():
    user_id = get_first_user_id()
    item = get_users_first_item(user_id)

    with open(TEST_IMG_PATH, "rb") as f:
        data = {"image": (f.name, f, "image/jpeg")}
        response = client.post(f"/users/{user_id}/items/{item}/file/", files=data)
    assert response.status_code == 200, f"{response.json()}"

    # Download image
    response = client.get(f"/users/{user_id}/items/{item}/file/", stream=True)
    assert response.status_code == 200

    # Check that an image was returned
    content_type = response.headers["content-type"]
    file_type, ext = content_type.split("/")
    assert file_type == "image"

    # Save image
    save_path = TEMP_DIR / f"downloaded.{ext}"
    with open(save_path, "wb") as f:
        for chunk in response:
            f.write(chunk)

    pass
