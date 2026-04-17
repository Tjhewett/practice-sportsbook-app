import pytest

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_field_goals(client):
    response = client.get('/api/field_goals?page=1&per_page=20')
    assert response.status_code == 200
    data = response.get_json()
    assert 'items' in data
    assert 'total' in data

def test_interceptions(client):
    response = client.get('/api/interceptions?page=1&per_page=20')
    assert response.status_code == 200
    data = response.get_json()
    assert 'items' in data
    assert 'total' in data

def test_passing(client):
    response = client.get('/api/passing?page=1&per_page=20')
    assert response.status_code == 200
    data = response.get_json()
    assert 'items' in data
    assert 'total' in data

def test_receiving(client):
    response = client.get('/api/receiving?page=1&per_page=20')
    assert response.status_code == 200
    data = response.get_json()
    assert 'items' in data
    assert 'total' in data

def test_rushing(client):
    response = client.get('/api/rushing?page=1&per_page=20')
    assert response.status_code == 200
    data = response.get_json()
    assert 'items' in data
    assert 'total' in data

def test_tackles(client):
    response = client.get('/api/tackles?page=1&per_page=20')
    assert response.status_code == 200
    data = response.get_json()
    assert 'items' in data
    assert 'total' in data

def test_team_passing(client):
    response = client.get('/api/team_passing?page=1&per_page=20')
    assert response.status_code == 200
    data = response.get_json()
    assert 'items' in data
    assert 'total' in data