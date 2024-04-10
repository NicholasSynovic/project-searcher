from argparse import Namespace
from string import Template
from typing import List

from requests import Response, get

from project_searcher.args import mainArgs

GITHUB_HEADERS: dict[str, str] = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
    "User-Agent": "prime-vX",
}

GITHUB_URL: Template = Template(
    template="https://api.github.com/search/repositories?q=size:${minSize}..${maxSize}+followers:${minFollowers}..${maxFollowers}+forks:${minForks}..${maxForks}+stars:${minStars}..${maxStars}&sort=${popularity}&order=${order}&per_page=100&page=${page}"
)


def getResponse(url: str, headers: dict) -> Response | None:
    resp: Response = get(url=url, headers=headers)

    if resp.status_code == 200:
        return resp
    else:
        return None


def githubSearch(args: Namespace, headers: dict[str, str]) -> None:
    page: int = 0

    while True:
        page += 1

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

        resp: Response | None = getResponse(url=url, headers=headers)

        if resp is None:
            quit(1)

        json: dict = resp.json()
        items: List[dict] = json["items"]

        item: dict
        for item in items:
            print(item["full_name"])


def main() -> None:
    args: Namespace = mainArgs()

    headers: dict
    match args.platform:
        case "github":
            headers = GITHUB_HEADERS
            headers["Authorization"] = f"Bearer {args.token}"
            githubSearch(args=args, headers=headers)
        case _:
            print("Invalid platform")
            quit(1)


if __name__ == "__main__":
    main()
