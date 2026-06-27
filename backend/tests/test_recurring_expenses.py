def test_create_recurring_expense(client, auth_headers):
    response = client.post(
        "/recurring-expenses",
        headers=auth_headers,
        json={
            "name": "Netflix",
            "amount": "39.90",
            "currency": "BRL",
            "billing_day": 15,
            "start_date": "2026-01-01",
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "Netflix"
    assert body["active"] is True


def test_create_recurring_expense_with_invalid_billing_day(client, auth_headers):
    response = client.post(
        "/recurring-expenses",
        headers=auth_headers,
        json={
            "name": "Academia",
            "amount": "100.00",
            "currency": "BRL",
            "billing_day": 40,
            "start_date": "2026-01-01",
        },
    )
    assert response.status_code == 400


def test_list_recurring_expenses(client, auth_headers):
    client.post(
        "/recurring-expenses",
        headers=auth_headers,
        json={
            "name": "Spotify",
            "amount": "21.90",
            "currency": "BRL",
            "billing_day": 5,
            "start_date": "2026-01-01",
        },
    )
    response = client.get("/recurring-expenses", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 1
