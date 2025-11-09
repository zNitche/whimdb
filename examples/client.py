import sys

sys.path.append(".")

from whimdb import Client


def main():
    client = Client(database_id=0, addr="0.0.0.0", port=8080, debug=True)

    s_response = client.set(key="test_key", value="test_value")
    s_response = client.set(key="test2_key", value="test2_value")
    q1_response = client.query(search_regex="(.*?)")
    q2_response = client.query(key="test_key")

    print(f"s_response: {s_response}")
    print(f"q1_response: {q1_response}")
    print(f"q2_response: {q2_response}")


if __name__ == "__main__":
    main()
