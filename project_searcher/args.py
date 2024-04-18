from argparse import ArgumentParser, HelpFormatter, Namespace
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

    # Flags
    parser.add_argument(
        "--git-clone",
        help="Flag to return git clone commands in a text file along with standard output",
        required=False,
        default=False,
        action="store_true",
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

    # Args with defaults
    parser.add_argument(
        "--popularity",
        help="Metric to determine popularity",
        type=str,
        required=False,
        choices=["stars", "forks"],
        default="stars",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Text file to store output",
        type=str,
        required=False,
        default="search.txt",
    )
    parser.add_argument(
        "--order",
        help="Order to present results. NOTE: Might cut off results if limit on search query",
        type=str,
        required=False,
        choices=["asc", "desc"],
        default="desc",
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

    return parser.parse_args()
