import sys
sys.path.append(".")


from whimdb import Server


def main():
    server = Server()

    try:
        server.run()
    
    except KeyboardInterrupt:
        server.stop()


if __name__ == "__main__":
    main()
