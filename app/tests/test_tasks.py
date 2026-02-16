from pytest import approx

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

def test_user_cannot_see_other_users(client):
    headers_a = get_auth_headers(client, email='user_a@example.com', password='password_a')

    client.post('/tasks', json={'title': 'task1', 'priority': 1}, headers=headers_a)
    client.post('/tasks', json={'title': 'task2', 'priority': 1}, headers=headers_a)

    headers_b = get_auth_headers(client, email='user_b@example.com', password='password_b')

    response = client.get('/tasks', headers=headers_b)

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 0

def test_user_cannot_update_other_users_tasks(client):
    headers_a = get_auth_headers(client, email='user_a@example.com', password='password_a')

    client.post('/tasks', json={'title': 'task1', 'priority': 1}, headers=headers_a)

    headers_b = get_auth_headers(client, email='user_b@example.com', password='password_b')

    response = client.put('/tasks/1', json={'title': 'test'}, headers=headers_b)

    assert response.status_code == 404

def test_user_cannot_delete_other_users_tasks(client):
    headers_a = get_auth_headers(client, email='user_a@example.com', password='password_a')

    client.post('/tasks', json={'title': 'task1', 'priority': 1}, headers=headers_a)

    headers_b = get_auth_headers(client, email='user_b@example.com', password='password_b')

    response = client.delete('/tasks/1', headers=headers_b)

    assert response.status_code == 404

def test_user_cannot_complete_other_users_tasks(client):
    headers_a = get_auth_headers(client, email='user_a@example.com', password='password_a')

    client.post('/tasks', json={'title': 'task1', 'priority': 1}, headers=headers_a)

    headers_b = get_auth_headers(client, email='user_b@example.com', password='password_b')

    response = client.patch('/tasks/1/complete', headers=headers_b)

    assert response.status_code == 404

def test_complete_tasks(client):
    headers = get_auth_headers(client)

    client.post('/tasks', json={'title': 'task1', 'priority': 1}, headers=headers)

    response = client.patch('/tasks/1/complete', headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'completed'
    assert data['completed_at'] is not None

    response = client.patch('/tasks/1/complete', headers=headers)
    assert response.status_code == 400

    response = client.patch('/tasks/1/reset', headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'pending'
    assert data['completed_at'] is None

    response = client.patch('/tasks/1/reset', headers=headers)
    assert response.status_code == 400

def test_update_tasks(client):
    headers = get_auth_headers(client)

    client.post('/tasks', json={'title': 'original', 'priority': 1}, headers=headers)

    response = client.put('/tasks/1', json={'title': 'updated title'}, headers=headers)
    assert response.status_code == 200

    data = response.json()

    assert data['title'] == 'updated title'
    assert data['priority'] == 1
    assert data['description'] is None
    assert data['status'] == 'pending'

    response = client.put('/tasks/1', json={'priority': 3}, headers=headers)
    data = response.json()
    assert data['priority'] == 3
    assert data['title'] == 'updated title'

def test_delete_tasks(client):
    headers = get_auth_headers(client)

    client.post('/tasks', json={'title': 'task1', 'priority': 1}, headers=headers)

    response = client.delete('/tasks/1', headers=headers)
    assert response.status_code == 204

    response = client.get('/tasks', headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0

    response = client.put('/tasks/1', json={'title': 'updated task', 'priority': 1}, headers=headers)
    assert response.status_code == 404

    response = client.patch('/tasks/1/complete', json={'title': 'test task', 'priority': 1}, headers=headers)
    assert response.status_code == 404

def test_task_stats(client):
    headers = get_auth_headers(client)

    client.post('/tasks', json={'title': 'task1', 'priority': 1}, headers=headers)
    client.post('/tasks', json={'title': 'task2', 'priority': 1}, headers=headers)
    client.post('/tasks', json={'title': 'task3', 'priority': 1}, headers=headers)

    response = client.patch('/tasks/2/complete', headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'completed'

    response = client.get('/tasks/stats', headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data['total'] == 3
    assert data['pending'] == 2
    assert data['completed'] == 1
    assert data['completion_rate'] == approx(33.33)

