def test_refund_stats_on_seeded_data(client):
    response = client.get("/stats/refunds")
    assert response.status_code == 200
    assert response.json() == {"refund_count": 1, "refunded_cents": 5000}


def test_refund_stats_after_new_refunds(client):
    for amount, key in [(1000, "stats-1"), (2000, "stats-2")]:
        response = client.post(
            "/orders/1001/refunds",
            json={"amount_cents": amount, "reason": "Item did not fit"},
            headers={"Idempotency-Key": key},
        )
        assert response.status_code == 201

    response = client.get("/stats/refunds")
    assert response.status_code == 200
    assert response.json() == {"refund_count": 3, "refunded_cents": 8000}
