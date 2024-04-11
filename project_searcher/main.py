from argparse import Namespace
from string import Template
from time import sleep, time
from typing import List, Tuple

from ghah.main import GH_REST
from progress.bar import Bar
from requests import Response

from project_searcher.args import mainArgs

GITHUB_URL: Template = Template(
    template="https://api.github.com/search/repositories?q=size:${minSize}..${maxSize}+followers:${minFollowers}..${maxFollowers}+forks:${minForks}..${maxForks}+stars:${minStars}..${maxStars}&sort=${popularity}&order=${order}&per_page=100&page=${page}"
)

DEFAULT_MESSAGE: str = "Conducting search..."
SLEEP_MESSAGE: str = "Sleeping for 60 seconds to avoid rate limit..."


def githubSearch(args: Namespace) -> List[dict]:
    data: List[dict] = []

    maxPage: int = 10
    totalTime: float = 0.0

    reqHeaders: dict[str, str] = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "prime-vX",
        "Authorization": f"Bearer {args.token}",
    }

    with Bar("Conducting search...", max=10) as bar:
        page: int
        for page in range(1, 11):
            # Handler for if the total time between API calls >= 15 seconds
            if totalTime >= 15:
                bar.message = SLEEP_MESSAGE
                bar.update()
                sleep(60)
                totalTime = 0.0
                bar.message = DEFAULT_MESSAGE
                bar.update()

            # Start time of the call
            startTime: float = time()

            url: str = GITHUB_URL.substitute(
                minSize=args.min_size,
                maxSize=args.max_size,
                minFollowers=args.min_followers,
                maxFollowers=args.max_followers,
                minForks=args.min_forks,
                maxForks=args.max_forks,
                minStars=args.min_stars,
                maxStars=args.max_stars,
                popularity=args.popularity,
                order=args.order,
                page=page,
            )

            # API handler
            gh: GH_REST = GH_REST(endpoint=url, reqHeaders=reqHeaders)
            resp: Tuple[Response, dict] = gh.get()
            # End time of the call
            endTime: float = time()

            # Total time it took for the call
            totalTime += endTime - startTime

            # Last page availible via pagination
            # NOTE: Only 1000 results are availible at a time. With 100 results
            # per page, that means that 1000 / 100 = 10 pages maximum returned
            lastPage: int = resp[1]["Last-Page"]
            maxPage = lastPage if (lastPage > 0) and (lastPage <= 10) else 10
            bar.max = maxPage
            bar.update()

            data.extend(resp[0].json()["items"])

            bar.next()

    return data


def main() -> None:
    args: Namespace = mainArgs()

    data: List[dict]
    match args.platform:
        case "github":
            data: List[dict] = githubSearch(args=args)
        case _:
            print("Invalid platform")
            quit(1)

    with open(file=args.output, mode="w") as txtFile:
        datum: dict
        for datum in data:
            name: str = datum["full_name"]
            txtFile.write(f"{name}\n")
        txtFile.close()


if __name__ == "__main__":
    main()
