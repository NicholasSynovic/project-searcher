from argparse import Namespace

from progress.bar import Bar
from requests import Response, get

from project_searcher.args import mainArgs


def main() -> None:
    args: Namespace = mainArgs()

    print(args)
    quit()


if __name__ == "__main__":
    main()
