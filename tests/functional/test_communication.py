from whimdb import Client


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
