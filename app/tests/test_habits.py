def get_auth_headers(client, email='user@example.com', password='test_password'):
    payload = {'email': email, 'password': password}
    client.post('/auth/register', json=payload)
    login_payload = {'username': email, 'password': password}
    response = client.post('/auth/login', data=login_payload)
    token = response.json()['access_token']
    return {'Authorization': f'Bearer {token}'}

def test_create_habit(client):
    headers = get_auth_headers(client)

    client.post('/habits', json={'name': 'habit', 'frequency': 'daily'}, headers=headers)

    response = client.get('/habits', headers=headers)

    assert response.status_code == 200

    data = response.json()

    assert data[0]['name'] == 'habit'
    assert data[0]['frequency'] == 'daily'
    assert data[0]['is_active'] == True

def test_get_habits(client):
    headers = get_auth_headers(client)

    client.post('/habits', json={'name': 'habit1', 'frequency': 'daily'}, headers=headers)
    client.post('/habits', json={'name': 'habit2', 'frequency': 'weekly'}, headers=headers)

    response = client.get('/habits', headers=headers)

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 2

def test_update_habit(client):
    headers = get_auth_headers(client)

    client.post('/habits', json={'name': 'habit1', 'frequency': 'daily'}, headers=headers)

    response = client.put('/habits/1', json={'name': 'new habit'}, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == 'new habit'
    assert data['frequency'] == 'daily'

    response = client.put('/habits/1', json={'frequency': 'weekly'}, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == 'new habit'
    assert data['frequency'] == 'weekly'

def test_delete_habit(client):
    headers = get_auth_headers(client)

    client.post('/habits', json={'name': 'habit1', 'frequency': 'daily'}, headers=headers)

    response = client.delete('/habits/1', headers=headers)
    assert response.status_code == 204

    response = client.get('/habits', headers=headers)
    data = response.json()
    assert len(data) == 0

def test_user_cannot_see_other_users_habit(client):
    headers_a = get_auth_headers(client, email='user_a@example.com', password='password_a')

    client.post('/habits', json={'name': 'habit1', 'frequency': 'daily'}, headers=headers_a)
    client.post('/habits', json={'name': 'habit2', 'frequency': 'daily'}, headers=headers_a)

    response = client.get('/habits', headers=headers_a)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2

    headers_b = get_auth_headers(client, email='user_b@example.com', password='password_b')

    response = client.get('/habits', headers=headers_b)

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 0

def test_user_cannot_update_other_users_habit(client):
    headers_a = get_auth_headers(client, email='user_a@example.com', password='password_a')

    client.post('/habits', json={'name': 'habit', 'frequency': 'daily'}, headers=headers_a)

    headers_b = get_auth_headers(client, email='user_b@example.com', password='password_b')

    response = client.put('habits/1', json={'name': 'updated habit'}, headers=headers_b)

    assert response.status_code == 404

def test_user_cannot_delete_other_users_habit(client):
    headers_a = get_auth_headers(client, email='user_a@example.com', password='password_a')

    response = client.post('/habits', json={'name': 'habit', 'frequency': 'daily'}, headers=headers_a)

    assert response.status_code == 200

    headers_b = get_auth_headers(client, email='user_b@example.com', password='password_b')

    response = client.delete('habits/1', headers=headers_b)

    assert response.status_code == 404

def test_user_cannot_log_other_users_habit(client):
    headers_a = get_auth_headers(client, email='user_a@example.com', password='password_a')

    response = client.post('/habits', json={'name': 'habit', 'frequency': 'daily'}, headers=headers_a)

    assert response.status_code == 200

    headers_b = get_auth_headers(client, email='user_b@example.com', password='password_b')

    response = client.post('/habits/1/log', json={}, headers=headers_b)

    assert response.status_code == 404

def test_log_daily_success(client):
    headers = get_auth_headers(client)

    response = client.post('/habits', json={'name': 'habit', 'frequency': 'daily'}, headers=headers)

    assert response.status_code == 200

    response = client.post('/habits/1/log', json={'log_date': '2026-03-02'}, headers=headers)

    assert response.status_code == 200

    response = client.post('/habits/1/log', json={'log_date': '2026-03-02'}, headers=headers)

    assert response.status_code == 400

def test_log_weekly_duplicate(client):
    headers = get_auth_headers(client)

    response = client.post('/habits', json={'name': 'habit', 'frequency': 'weekly'}, headers=headers)

    assert response.status_code == 200

    response = client.post('/habits/1/log', json={'log_date': '2026-03-02'}, headers=headers)

    assert response.status_code == 200

    response = client.post('/habits/1/log', json={'log_date': '2026-03-05'}, headers=headers)

    assert response.status_code == 400

def test_log_weekly_success(client):
    headers = get_auth_headers(client)

    response = client.post('/habits', json={'name': 'habit', 'frequency': 'weekly'}, headers=headers)

    assert response.status_code == 200

    response = client.post('/habits/1/log', json={'log_date': '2026-03-02'}, headers=headers)

    assert response.status_code == 200

    response = client.post('/habits/1/log', json={'log_date': '2026-03-09'}, headers=headers)

    assert response.status_code == 200

def test_delete_habit_cascade_logs(client):
    headers = get_auth_headers(client)

    response = client.post('habits', json={'name': 'habit', 'frequency': 'daily'}, headers=headers)
    assert response.status_code == 200

    response = client.post('habits/1/log', json={'log_date': '2026-03-02'}, headers=headers)
    assert response.status_code == 200

    response = client.delete('/habits/1', headers=headers)
    assert response.status_code == 204

    response = client.post('/habits/1/log', json={'log_date': '2026-03-02'}, headers=headers)
    assert response.status_code == 404
