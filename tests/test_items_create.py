def test_create_item(client):
    response = client.post("/items?name=banana")

    assert response.status_code == 200
    data = response.json()

    assert data["name"] == "banana"
    assert "id" in data
