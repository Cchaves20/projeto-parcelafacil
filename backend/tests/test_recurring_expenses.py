def test_create_recurring_expense(client):
    response = client.post(
        "/recurring-expenses",
        json={
            "name": "Netflix",
            "amount": "39.90",
            "currency": "BRL",
            "frequency": "MONTHLY",
            "billing_day": 15,
            "periods": [{"start_date": "2026-01-01"}],
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "Netflix"
    assert body["active"] is True


def test_create_recurring_expense_with_invalid_billing_day(client):
    response = client.post(
        "/recurring-expenses",
        json={
            "name": "Academia",
            "amount": "100.00",
            "currency": "BRL",
            "frequency": "MONTHLY",
            "billing_day": 40,
            "periods": [{"start_date": "2026-01-01"}],
        },
    )
    assert response.status_code == 400


def test_create_weekly_recurring_expense_requires_weekdays(client):
    response = client.post(
        "/recurring-expenses",
        json={
            "name": "Comida da faculdade",
            "amount": "40.00",
            "currency": "BRL",
            "frequency": "WEEKLY",
            "periods": [{"start_date": "2026-03-01", "end_date": "2026-06-30"}],
        },
    )
    assert response.status_code == 400


def test_create_weekly_recurring_expense_with_multiple_periods(client):
    response = client.post(
        "/recurring-expenses",
        json={
            "name": "Comida da faculdade",
            "amount": "40.00",
            "currency": "BRL",
            "frequency": "WEEKLY",
            "weekdays": [0, 1, 2, 3],
            "periods": [
                {"start_date": "2026-03-01", "end_date": "2026-06-30"},
                {"start_date": "2026-08-01", "end_date": "2026-12-10"},
            ],
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["weekdays"] == [0, 1, 2, 3]
    assert len(body["periods"]) == 2


def test_list_recurring_expenses(client):
    client.post(
        "/recurring-expenses",
        json={
            "name": "Spotify",
            "amount": "21.90",
            "currency": "BRL",
            "frequency": "MONTHLY",
            "billing_day": 5,
            "periods": [{"start_date": "2026-01-01"}],
        },
    )
    response = client.get("/recurring-expenses")
    assert response.status_code == 200
    assert len(response.json()) == 1
