from whimdb import Client
from whimdb.dataclasses.communication import QueryItem


def test_echo(client: Client, server):
    res = client.echo()

    assert res == True


def test_purge(client: Client, server):
    res = client.purge()

    assert res == True


def test_set(client: Client, server):
    res = client.set(key="test2_key", value="test2_value")

    assert res == True


def test_remove(client: Client, server):
    res_success = client.remove(key="test2_key")
    res_fail = client.remove(key="test2_key_2")

    assert res_success == True
    assert res_fail == True


def test_empty_query(client: Client, server):
    res = client.query(search_regex="(.*?)")

    assert res == None


def test_query(client: Client, server):
    res = client.set(key="test2_key", value="test2_value")
    res = client.query(search_regex="(.*?)")

    assert res != None
    assert len(res.value) == 1  # type: ignore
    assert type(res.value[0]) == QueryItem  # type: ignore


def test_update_ttl(client: Client, server):
    key = "test_update_ttl_key"
    value = "test_update_ttl_value"

    client.set(key=key, value=value, ttl=None)
    client.update_ttl(key=key, ttl=30)

    res = client.query(key=key)

    assert res != None
    assert len(res.value) == 1  # type: ignore

    item = res.value[0] # type: ignore

    assert item.ttl == 30
    assert item.value == value

