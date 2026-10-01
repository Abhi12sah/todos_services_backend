def test_create_user(client):
    response = client.post(
        "/users/",
        json={
            "name": "Test User",
            "email": "testuser@example.com",
            "password": "TestPass123"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Test User"
    assert data["email"] == "testuser@example.com"
    assert "id" in data


def test_get_users(client):
    response = client.get("/users/")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


def test_get_user(client):
    create_response = client.post(
        "/users/",
        json={
            "name": "Get User",
            "email": "getuser@example.com",
            "password": "TestPass123"
        }
    )

    assert create_response.status_code == 201

    user_id = create_response.json()["id"]

    response = client.get(f"/users/{user_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == user_id
    assert data["name"] == "Get User"
    assert data["email"] == "getuser@example.com"


def test_update_user(client):
    create_response = client.post(
        "/users/",
        json={
            "name": "Old Name",
            "email": "updateuser@example.com",
               "password": "TestPass123"
        }
    )

    assert create_response.status_code == 201

    user_id = create_response.json()["id"]

    response = client.patch(
        f"/users/{user_id}",
        json={
            "name": "Updated Name"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == user_id
    assert data["name"] == "Updated Name"


def test_delete_user(client):
    create_response = client.post(
        "/users/",
        json={
            "name": "Delete User",
            "email": "deleteuser@example.com",
            "password": "TestPass123"
        }
    )

    assert create_response.status_code == 201

    user_id = create_response.json()["id"]

    response = client.delete(f"/users/{user_id}")

    assert response.status_code in [200, 204]

    get_response = client.get(f"/users/{user_id}")

    assert get_response.status_code == 404


def test_duplicate_email(client):
    user = {
        "name": "Duplicate User",
        "email": "duplicate@example.com",
        "password": "TestPass123"
    }

    first_response = client.post(
        "/users/",
        json=user
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/users/",
        json=user
    )

    assert second_response.status_code == 409