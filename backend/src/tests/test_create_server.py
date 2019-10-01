import pytest
from pprint import pprint
from dotmap import DotMap
import numbers

discord_prefix = "/api/discord"


@pytest.fixture()
def create_d_server_custom(client):
    def create(json):
        if "name" not in json:
            json["name"] = "aName"
        if "id" not in json:
            json["id"] = 1
        res = client.post(discord_prefix, json=json)
        assert res == 200
        return res

    return create


@pytest.fixture()
def create_d_server(create_d_server_custom):
    return create_d_server_custom({"name": "aName", "id": 42069})


route = f"{discord_prefix}/42069"


def compare_server_response(response, expected):
    __tracebackhide__ = True
    for key in expected:
        if key not in expected:
            pytest.fail("expected response to have key ({key})")
        if not expected[key] == response[key]:
            pytest.fail(
                f"expected respose[{key}] to equal ({expected[key]}) but got ({response[key]})"
            )


def test_create(client, create_d_server_custom):
    expectedServerRes = {
        "name": "aName",
        "command_prefixes": None,
        "message_prefixes": None,
        "id": 10,
        "server_group_id": 1,
        "admin_role": None,
    }
    res = client.get(discord_prefix)
    assert len(res.json) == 0
    assert res == 200
    res = client.get(f"{discord_prefix}/10")
    assert res == 404
    res = create_d_server_custom({"name": "aName", "id": 10})
    assert res == 200
    compare_server_response(res.json, expectedServerRes)
    res = client.get(discord_prefix)
    assert res == 200
    assert len(res.json) == 1
    compare_server_response(res.json[0], expectedServerRes)


def test_get_server(client, create_d_server):
    server = DotMap(create_d_server.json)
    res = client.get(route)
    assert res == 200
    assert res.json == server


def test_set_admin_role(client, create_d_server):
    server = DotMap(create_d_server.json)
    expectedServerRes = DotMap(
        {
            "name": "aName",
            "command_prefixes": None,
            "message_prefixes": None,
            "id": 42069,
            "server_group_id": 1,
            "admin_role": 42,
        }
    )

    assert server.admin_role == None
    res = client.put(route, json={"admin_role": 42})
    assert res == 200
    compare_server_response(res.json, expectedServerRes)


def test_add_command_prefix(client, create_d_server):
    server = DotMap(create_d_server.json)
    expectedServerRes = DotMap(
        {
            "name": "aName",
            "command_prefixes": ["!"],
            "message_prefixes": None,
            "id": 42069,
            "server_group_id": 1,
            "admin_role": None,
        }
    )

    assert server.admin_role == None
    res = client.put(route, json={"command_prefix": "!"})
    assert res == 200
    compare_server_response(res.json, expectedServerRes)
    res = client.put(route, json={"command_prefix": "?"})
    expectedServerRes.command_prefixes.append("?")
    compare_server_response(res.json, expectedServerRes)
