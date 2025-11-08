import sys
sys.path.append(".")


from whimdb import Server


def main():
    server = Server(port=8080, debug=True)

    try:
        server.start()
    
    except KeyboardInterrupt:
        server.stop()


if __name__ == "__main__":
    main()
