def test_create_list_update_and_delete_user(client) -> None:
    create_payload = {'email': 'ana@example.com', 'name': 'Ana'}
    create_response = client.post('/v1/users', json=create_payload)

    assert create_response.status_code == 201
    created_user = create_response.json()
    assert created_user['email'] == create_payload['email']
    assert created_user['name'] == create_payload['name']

    list_response = client.get('/v1/users')
    assert list_response.status_code == 200
    users = list_response.json()
    assert len(users) == 1
    assert users[0]['id'] == created_user['id']

    update_response = client.patch(
        f"/v1/users/{created_user['id']}",
        json={'email': 'ana.silva@example.com', 'name': 'Ana Silva'},
    )
    assert update_response.status_code == 200
    assert update_response.json()['name'] == 'Ana Silva'

    delete_response = client.delete(f"/v1/users/{created_user['id']}")
    assert delete_response.status_code == 204

    empty_list_response = client.get('/v1/users')
    assert empty_list_response.status_code == 200
    assert empty_list_response.json() == []


def test_update_and_delete_missing_user_returns_404(client) -> None:
    update_response = client.patch('/v1/users/999', json={'email': 'ghost@example.com', 'name': 'Ghost'})
    assert update_response.status_code == 404
    assert update_response.json() == {'detail': 'User not found'}

    delete_response = client.delete('/v1/users/999')
    assert delete_response.status_code == 404
    assert delete_response.json() == {'detail': 'User not found'}
