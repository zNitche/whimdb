import threading
from whimdb import Server, Client


def get_server(port=8080):
    server = Server(port=port)

    thread = threading.Thread(target=server.start)
    thread.start()

    return server, thread


def stop_server(server: Server, thread: threading.Thread):
    server.stop()
    thread.join()


def get_client(port=8080):
    return Client(database_id=0, addr="0.0.0.0", port=port)
