import sys
sys.path.append(".")

import time
import threading
from whimdb import Client


def run_client(client_id: int):
    client = Client(database_id=0, addr="0.0.0.0", port=8080, debug=False)

    print(f"started client {client_id}")
    start_time = time.time()

    response = client.query(key="123")

    end_time = round(time.time() - start_time, 2)
    print(f"request took: {end_time},res: {response}")


def main():
    clients_count = 10

    clients_threads = [threading.Thread(
        target=run_client, args=[id]) for id in range(clients_count)]
    
    for thread in clients_threads:
        thread.start()


if __name__ == "__main__":
    main()
