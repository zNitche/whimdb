import pytest
import time
from tests.modules import get_server, stop_server, get_client


@pytest.fixture(scope="module")
def server():
    client = get_client()
    server, server_thread = get_server()

    # wait for server to come online
    while True:
        try:
            res = client.echo()

            if res:
                break

        except ConnectionRefusedError:
            pass

        time.sleep(1)

    yield

    stop_server(server, server_thread)


@pytest.fixture(scope="function")
def client():
    return get_client()
