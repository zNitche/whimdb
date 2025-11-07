import sys
sys.path.append(".")

from whimdb import Client


def main():
    client = Client(addr="0.0.0.0", port=8080, debug=True)

    with client:
        response = client.query(key="123")

        if response:
            print(response.content)


if __name__ == "__main__":
    main()
