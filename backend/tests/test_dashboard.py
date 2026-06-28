from decimal import Decimal

from app.services import currency_service


def test_dashboard_summary_converts_usd_income_to_brl(client, monkeypatch):
    monkeypatch.setattr(currency_service, "get_usd_to_brl_rate", lambda: Decimal("5.00"))

    client.post(
        "/users/me/incomes",
        json={"description": "Salário", "amount": "1000.00", "currency": "BRL"},
    )
    client.post(
        "/users/me/incomes",
        json={"description": "Freela", "amount": "200.00", "currency": "USD"},
    )
    client.post(
        "/recurring-expenses",
        json={
            "name": "Netflix",
            "amount": "50.00",
            "currency": "BRL",
            "frequency": "MONTHLY",
            "billing_day": 10,
            "periods": [{"start_date": "2026-01-01"}],
        },
    )

    response = client.get("/dashboard/summary", params={"year": 2026, "month": 1})
    assert response.status_code == 200
    body = response.json()

    assert body["monthly_income_brl"] == "2000.00"
    assert body["recurring_expenses_brl"] == "50.00"
    assert body["committed_percentage"] == "2.50"


def test_dashboard_summary_with_no_income_returns_zero_percentage(client):
    response = client.get("/dashboard/summary", params={"year": 2026, "month": 1})
    assert response.status_code == 200
    assert response.json()["committed_percentage"] == "0"


def test_dashboard_summary_counts_weekly_expense_occurrences_in_active_period(client):
    client.post(
        "/users/me/incomes",
        json={"description": "Salário", "amount": "1000.00", "currency": "BRL"},
    )
    client.post(
        "/recurring-expenses",
        json={
            "name": "Comida da faculdade",
            "amount": "40.00",
            "currency": "BRL",
            "frequency": "WEEKLY",
            "weekdays": [0, 1, 2, 3],
            "periods": [{"start_date": "2026-03-01", "end_date": "2026-06-30"}],
        },
    )

    response = client.get("/dashboard/summary", params={"year": 2026, "month": 3})
    assert response.status_code == 200
    body = response.json()
    assert body["recurring_expenses_brl"] == "720.00"
