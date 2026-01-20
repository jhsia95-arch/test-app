def test_delete_item(client):
    create = client.post("/items?name=to-delete")
    item_id = create.json()["id"]

    delete = client.delete(f"/items/{item_id}")
    assert delete.status_code == 200

    get_all = client.get("/items")
    ids = [item["id"] for item in get_all.json()]
    assert item_id not in ids
