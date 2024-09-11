def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert "Hello" in response.data.decode('utf-8')


def test_hello_name(client):
    response = client.get("/hello/<name>/")
    assert response.status_code == 200
    assert "Hello" in response.data.decode('utf-8')   