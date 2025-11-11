import sys
sys.path.append(".")

import time
import threading
from whimdb import Client


def run_client(client_id: int):
    client = Client(database_id=0, addr="0.0.0.0", port=8080, debug=False)

    print(f"started client {client_id}")
    start_time = time.time()

    s_response = client.set(key=f"test_key_{client_id}", value="test_value")
    s_response = client.set(key=f"test2_key_{client_id}", value="test2_value", ttl=10)
    q1_response = client.query(search_regex="(.*?)")
    q2_response = client.query(key=f"test_key_{client_id}")

    end_time = round(time.time() - start_time, 2)
    print(f"[{client_id}] request took: {end_time}")


def main():
    # 300 client * 4 requests per client = 1200 simultaneous requests
    clients_count = 300

    clients_threads = [threading.Thread(
        target=run_client, args=[id]) for id in range(clients_count)]
    
    for thread in clients_threads:
        thread.start()


if __name__ == "__main__":
    main()
