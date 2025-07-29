import argparse

from bundecto import __version__
from bundecto.editor import main


def run_editor():
    parser = argparse.ArgumentParser(
        prog="bundecto", description="A curses-based minimal text editor."
    )

    parser.add_argument("filename", nargs="?", help="File to open in the editor")

    parser.add_argument(
        "-r", "--readonly", action="store_true", help="Open the file in read-only mode"
    )

    parser.add_argument(
        "--no-stty-xon",
        action="store_false",
        help="Disable raw input mode; use 'cooked' input handling instead",
    )

    parser.add_argument(
        "-v", "--version", action="version", version=f"%(prog)s {__version__}"
    )

    args = parser.parse_args()

    main(args.filename, readonly=args.readonly, allow_raw=args.no_stty_xon)


if __name__ == "__main__":
    run_editor()
