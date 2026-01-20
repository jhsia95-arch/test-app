def test_update_item(client):
    create = client.post("/items?name=old")
    item_id = create.json()["id"]

    update = client.put(f"/items/{item_id}?name=new")
    assert update.status_code == 200
    assert update.json()["name"] == "new"
