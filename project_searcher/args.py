from argparse import ArgumentParser, HelpFormatter, Namespace
from datetime import datetime
from operator import attrgetter


class SortingHelpFormatter(HelpFormatter):
    def add_arguments(self, actions):
        actions = sorted(actions, key=attrgetter("option_strings"))
        super(SortingHelpFormatter, self).add_arguments(actions)


AUTHORS: list = [
    "Nicholas M. Synovic",
    "Matthew Hyatt",
    "George K. Thiruvathukal",
]

MAX_VALUE: int = 1000000000
MIN_VALUE: int = 0


def mainArgs() -> Namespace:
    parser: ArgumentParser = ArgumentParser(
        prog=f"Software Project Searcher",
        description="Command line tool for searching for software projects on code hosting platforms",
        epilog=f"Author(s): {', '.join(AUTHORS)}",
        formatter_class=SortingHelpFormatter,
    )

    # Required args
    parser.add_argument(
        "-t",
        "--token",
        help="Code hosting platform API token",
        type=str,
        required=True,
    )
    parser.add_argument(
        "-p",
        "--platform",
        help="Code hosting platform name",
        type=str,
        choices=["github"],
        default="github",
    )

    # Repo language, has default value that can limit the search results
    parser.add_argument(
        "--language",
        help="Language of code in a repository",
        type=str,
        required=False,
        default="java",
    )

    # Repo size
    parser.add_argument(
        "--min-size",
        help="Minimum size of repository in kilobytes",
        type=int,
        required=False,
        default=MIN_VALUE,
    )
    parser.add_argument(
        "--max-size",
        help="Maximum size of repository in MB",
        type=int,
        required=False,
        default=MAX_VALUE,
    )

    # Repo followers
    parser.add_argument(
        "--min-followers",
        help="Minimum number of followers a repository must have",
        type=int,
        required=False,
        default=MIN_VALUE,
    )
    parser.add_argument(
        "--max-followers",
        help="Maximum number of followers a repository must have",
        type=int,
        required=False,
        default=MAX_VALUE,
    )

    # Repo forks
    parser.add_argument(
        "--min-forks",
        help="Minimum number of forks a repository must have",
        type=int,
        required=False,
        default=MIN_VALUE,
    )
    parser.add_argument(
        "--max-forks",
        help="Maximum number of forks a repository must have",
        type=int,
        required=False,
        default=MAX_VALUE,
    )

    # Repo stars
    parser.add_argument(
        "--min-stars",
        help="Minimum number of stars a repository must have",
        type=int,
        required=False,
        default=MIN_VALUE,
    )
    parser.add_argument(
        "--max-stars",
        help="Maximum number of stars a repository must have",
        type=int,
        required=False,
        default=MAX_VALUE,
    )

    # Repo creation/ updated
    parser.add_argument(
        "--min-created-date",
        help="Minimum date of creation a repository must have",
        type=str,
        required=False,
        default="1970-01-01",
    )
    parser.add_argument(
        "--max-created-date",
        help="Maximum date of creation a repository must have",
        type=str,
        required=False,
        default=datetime.now().strftime("%Y-%m-%d"),
    )
    parser.add_argument(
        "--min-pushed-date",
        help="Minimum date of the latest push a repository must have",
        type=str,
        required=False,
        default="1970-01-01",
    )
    parser.add_argument(
        "--max-pushed-date",
        help="Maximum date of the latest push a repository must have",
        type=str,
        required=False,
        default=datetime.now().strftime("%Y-%m-%d"),
    )

    return parser.parse_args()
