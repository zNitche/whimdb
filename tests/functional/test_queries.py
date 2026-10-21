from whimdb import Client
from whimdb.dataclasses.communication import QueryItem


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

    res = client.query(key=key)

    assert res != None
    assert len(res.value) == 1  # type: ignore

    item = res.value[0]  # type: ignore

    assert item.value == value


def test_query_pages(client: Client, server):
    client.purge()

    # 8 pages with 15 items + 1 page with 8
    for id in range(128):
        client.set(key=f"key_{id}", value=f"value_{id}")

    queried_pages = 0
    queried_items = 0

    for page in client.query_pages(search_regex="(.*?)", items_per_page=15):
        assert page != None

        queried_pages += 1
        queried_items += len(page)

    assert queried_pages == 9
    assert queried_items == 128


def test_key_count(client: Client, server):
    TARGET_KEY_COUNT = 21

    client.purge()

    for id in range(TARGET_KEY_COUNT):
        client.set(key=f"key_{id}", value=f"value_{id}")

    key_count = client.db_key_count()

    assert key_count == TARGET_KEY_COUNT
