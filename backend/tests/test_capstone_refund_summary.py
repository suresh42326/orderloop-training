def test_ac1_existing_order_has_summary_fields(client):
    response = client.get('/orders/1007/refund-summary')
    assert response.status_code == 200
    assert set(response.json()) == {'order_id', 'refund_count', 'refunded_cents', 'remaining_cents', 'last_refund_at'}
    assert response.json()['order_id'] == 1007


def test_ac2_order_without_refunds(client):
    data = client.get('/orders/1001/refund-summary').json()
    assert data['refund_count'] == 0
    assert data['refunded_cents'] == 0
    assert data['last_refund_at'] is None


def test_ac3_unknown_order(client):
    response = client.get('/orders/999/refund-summary')
    assert response.status_code == 404
    assert response.json()['detail']['code'] == 'order_not_found'


def test_ac4_no_personal_data_or_reason(client):
    response = client.get('/orders/1007/refund-summary')
    assert set(response.json()) == {'order_id', 'refund_count', 'refunded_cents', 'remaining_cents', 'last_refund_at'}


def test_ac5_multiple_refunds_and_remaining(client):
    response = client.post('/orders/1007/refunds', json={'amount_cents': 1000, 'reason': 'item damaged'}, headers={'Idempotency-Key': 'summary-test'})
    assert response.status_code == 201
    summary = client.get('/orders/1007/refund-summary').json()
    assert summary['refund_count'] == 2
    assert summary['refunded_cents'] == 6000
    assert summary['remaining_cents'] == 9000
    assert summary['last_refund_at'] == '2030-03-01T10:00:00'
