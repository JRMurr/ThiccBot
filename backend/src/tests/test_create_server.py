# import pytest
from pprint import pprint


def test_create(client):
    res = client.get("/api/discord")
    assert len(res.json) == 0
    assert res == 200
    res = client.get("/api/discord/10")
    assert res == 404
    res = client.post("api/discord", json={"name": "aName", "id": 10})
    assert res == 200
    assert res.json == {
        "name": "aName",
        "command_prefixes": None,
        "message_prefixes": None,
        "server_group_id": 1,
        "id": 10,
        "admin_role": None,
    }
