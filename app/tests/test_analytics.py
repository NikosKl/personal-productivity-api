from pytest import approx

def get_auth_headers(client, email='user@example.com', password='test_password'):
    payload = {'email': email, 'password': password}
    client.post('auth/register', json=payload)
    login_payload = {'username': email, 'password': password}
    response = client.post('auth/login', data=login_payload)
    token = response.json()['access_token']
    return {'Authorization': f'Bearer {token}'}

def test_analytics_summary(client):
    headers = get_auth_headers(client)

    client.post('/tasks', json={'title': 'task1', 'priority': 1}, headers=headers)
    client.post('/tasks', json={'title': 'task2', 'priority': 2}, headers=headers)
    client.post('/tasks', json={'title': 'task3', 'priority': 3}, headers=headers)
    response = client.get('/tasks', headers=headers)
    data = response.json()
    assert len(data) == 3
    response = client.patch('/tasks/1/complete', headers=headers)
    data = response.json()
    assert data['status'] == 'completed'
    assert data['completed_at'] is not None

    client.post('/habits', json={'name': 'habit1', 'frequency': 'daily'}, headers=headers)
    client.post('/habits', json={'name': 'habit2', 'frequency': 'weekly'}, headers=headers)
    response = client.get('/habits', headers=headers)
    data = response.json()
    assert len(data) == 2
    response = client.put('/habits/1', json={'is_active': False}, headers=headers)
    data = response.json()
    assert data['is_active'] is False

    client.post('/habits/1/log', json={'log_date': '2026-03-02'}, headers=headers)
    client.post('/habits/1/log', json={'log_date': '2026-03-03'}, headers=headers)
    client.post('/habits/1/log', json={'log_date': '2026-03-04'}, headers=headers)
    client.post('/habits/2/log', json={'log_date': '2026-03-03'}, headers=headers)
    client.post('/habits/2/log', json={'log_date': '2026-03-10'}, headers=headers)
    response = client.get('/habits/1/streak', headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data['habit_id'] == 1
    assert data['current_streak'] == 3

    response = client.get('/analytics/summary', headers=headers)
    data = response.json()

    assert data['tasks']['total'] == 3
    assert data['tasks']['completed'] == 1
    assert data['tasks']['pending'] == 2
    assert data['tasks']['completion_rate'] == approx(33.33)
    assert data['habits']['total'] == 2
    assert data['habits']['active'] == 1
    assert data['habits']['total_logs'] == 5
    assert data['habits']['longest_streak'] == 3

