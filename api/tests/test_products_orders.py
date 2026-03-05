def test_create_and_list_products(client) -> None:
    create_response = client.post(
        '/v1/products',
        json={'sku': 'SKU-1', 'name': 'Teclado Mecânico', 'price': 199.9},
    )

    assert create_response.status_code == 201
    created_product = create_response.json()
    assert created_product['sku'] == 'SKU-1'

    list_response = client.get('/v1/products')
    assert list_response.status_code == 200
    products = list_response.json()
    assert len(products) == 1
    assert products[0]['id'] == created_product['id']


def test_create_and_list_orders(client) -> None:
    user = client.post('/v1/users', json={'email': 'order-user@example.com', 'name': 'Order User'}).json()
    product = client.post('/v1/products', json={'sku': 'SKU-ORDER', 'name': 'Mouse', 'price': 99.9}).json()

    create_order_response = client.post(
        '/v1/orders',
        json={'user_id': user['id'], 'product_id': product['id'], 'quantity': 2},
    )

    assert create_order_response.status_code == 201
    created_order = create_order_response.json()
    assert created_order['quantity'] == 2

    list_response = client.get('/v1/orders')
    assert list_response.status_code == 200
    orders = list_response.json()
    assert len(orders) == 1
    assert orders[0]['id'] == created_order['id']


def test_order_validation_rejects_invalid_quantity(client) -> None:
    user = client.post('/v1/users', json={'email': 'validation-user@example.com', 'name': 'Validation User'}).json()
    product = client.post('/v1/products', json={'sku': 'SKU-VAL', 'name': 'Monitor', 'price': 1000.0}).json()

    response = client.post(
        '/v1/orders',
        json={'user_id': user['id'], 'product_id': product['id'], 'quantity': 0},
    )

    assert response.status_code == 422
