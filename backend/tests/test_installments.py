def test_create_installment_purchase_generates_installments(client, auth_headers):
    response = client.post(
        "/installment-purchases",
        headers=auth_headers,
        json={
            "description": "Notebook",
            "total_amount": "1000.00",
            "currency": "BRL",
            "installments_count": 3,
            "first_due_date": "2026-01-10",
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["installments_count"] == 3
    assert len(body["installments"]) == 3
    assert [item["due_date"] for item in body["installments"]] == ["2026-01-10", "2026-02-10", "2026-03-10"]
    assert sum(float(item["amount"]) for item in body["installments"]) == 1000.00


def test_installment_amounts_absorb_rounding_remainder(client, auth_headers):
    response = client.post(
        "/installment-purchases",
        headers=auth_headers,
        json={
            "description": "Celular",
            "total_amount": "100.00",
            "currency": "BRL",
            "installments_count": 3,
            "first_due_date": "2026-01-31",
        },
    )
    body = response.json()
    amounts = [item["amount"] for item in body["installments"]]
    assert amounts[0] == amounts[1] == "33.33"
    assert amounts[2] == "33.34"
    due_dates = [item["due_date"] for item in body["installments"]]
    assert due_dates == ["2026-01-31", "2026-02-28", "2026-03-31"]
