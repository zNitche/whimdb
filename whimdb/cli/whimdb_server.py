import argparse
from whimdb import Server


def main(args: argparse.Namespace):
    server = Server(port=args.port, addr=args.addr, debug=args.debug)
    server.start()


def get_args():
    argument_parser = argparse.ArgumentParser()

    argument_parser.add_argument(
        "--port", type=int, default=8080, help="server port", required=False)
    argument_parser.add_argument(
        "--addr", type=str, default="0.0.0.0", help="server address", required=False)

    argument_parser.add_argument("--debug", action=argparse.BooleanOptionalAction,
                                 default=False, help="debug mode", required=False)

    return argument_parser.parse_args()


def run():
    args = get_args()

    main(args)
