def test_health_check(client):
    """Test the /health endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data == {"status": "healthy"}

def test_create_task(client):
    """Test creating a task."""
    response = client.post('/api/', json={"name": "Test Task", "description": "This is a test task."})
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Test Task"
    assert data["description"] == "This is a test task."

def test_get_tasks(client):
    """Test retrieving tasks."""
    client.post('/api/', json={"name": "Test Task", "description": "This is a test task."})

    response = client.get('/api/')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["name"] == "Test Task"
