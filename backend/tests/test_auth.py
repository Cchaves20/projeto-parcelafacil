def test_register_and_login(client):
    register_response = client.post(
        "/auth/register", json={"name": "Caio", "email": "caio@example.com", "password": "senha123"}
    )
    assert register_response.status_code == 201

    login_response = client.post("/auth/login", json={"email": "caio@example.com", "password": "senha123"})
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()


def test_login_with_wrong_password(client):
    client.post("/auth/register", json={"name": "Caio", "email": "caio@example.com", "password": "senha123"})
    response = client.post("/auth/login", json={"email": "caio@example.com", "password": "errada"})
    assert response.status_code == 401


def test_me_requires_authentication(client):
    response = client.get("/users/me")
    assert response.status_code == 401
