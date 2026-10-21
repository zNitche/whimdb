import sys
sys.path.append(".")

import time
import threading
from whimdb import Client


def run_client(client_id: int):
    client = Client(database_id=0, addr="0.0.0.0", port=8080, debug=False)

    print(f"started client {client_id}")
    start_time = time.time()

    client.set(key=f"test_key_{client_id}", value=f"test_value_{client_id}")
    client.set(key=f"test{client_id}_key_{client_id}",
                            value=f"test{client_id}_value_{client_id}", ttl=10)
    client.query(search_regex="(.*?)")
    client.query(key=f"test_key_{client_id}")

    end_time = round(time.time() - start_time, 2)
    print(f"[{client_id}] request took: {end_time}")


def main():
    # 300 client * 4 requests per client = 1200 simultaneous requests
    clients_count = 300

    clients_threads = [threading.Thread(
        target=run_client, args=[id]) for id in range(clients_count)]
    
    for thread in clients_threads:
        thread.start()

    for thread in clients_threads:
        thread.join()


if __name__ == "__main__":
    main()
