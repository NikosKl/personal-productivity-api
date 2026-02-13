def get_auth_headers(client, email='user@example.com', password='test_password'):
    payload = {'email': email, 'password': password}
    client.post('/auth/register', json=payload)
    login_payload = {'username': email, 'password': password}
    response = client.post('/auth/login', data=login_payload)
    token = response.json()['access_token']
    return {'Authorization': f'Bearer {token}'}

def test_authenticate_user(client):

    headers = get_auth_headers(client)

    response = client.post('/tasks', json={'title': 'test task', 'priority': 1}, headers=headers)

    assert response.status_code == 200

    data = response.json()

    assert data['title'] == 'test task'
    assert data['status'] == 'pending'
    assert data['completed_at'] is None

def test_get_tasks(client):
    headers = get_auth_headers(client)

    client.post('/tasks', json={'title': 'task1', 'priority': 1}, headers=headers)
    client.post('/tasks', json={'title': 'task2', 'priority': 1}, headers=headers)

    response = client.get('/tasks', headers=headers)

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 2

    for task in data:
        assert task['title'] in ['task1', 'task2']



