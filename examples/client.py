import sys
sys.path.append(".")


from whimdb import Client


def main():
    client = Client(addr="0.0.0.0", port=8080, debug=True)

    with client:
        pass


if __name__ == "__main__":
    main()
