def test_register(client):
    response = client.post('/auth/register',
                           json={
                               'email': 'test_user@example.com',
                               'password': 'longpassword'})

    assert response.status_code in (200, 201)

    data = response.json()

    assert 'id' in data
    assert 'email' in data
    assert 'password_hash' not in data

def test_duplicate_email(client):
    payload = {'email': 'test_user@example.com', 'password': 'testpassword'}

    client.post('/auth/register', json=payload)

    response = client.post('/auth/register', json=payload)
    assert response.status_code == 409

def test_login_success(client):
    payload ={'email': 'login_success@example.com', 'password': 'correctpassword'}
    client.post('/auth/register', json=payload)

    response = client.post('/auth/login', data={'username': payload['email'], 'password': payload['password']})

    assert response.status_code == 200
    data = response.json()
    assert 'access_token' in data
    assert data['token_type'] == 'bearer'

def test_login_failure(client):
    payload = {'email': 'login_failure@example.com', 'password': 'correctpassword'}
    client.post('/auth/register', json=payload)

    response = client.post('/auth/login', data={'username': 'login_failure@example.com', 'password': 'wrongpassword'})

    assert response.status_code == 401







