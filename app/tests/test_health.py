def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()
    assert 'name' in data
    assert 'version' in data
    assert 'environment' in data