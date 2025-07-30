import sys

from .decoder import decode_url


def main() -> None:
    if len(sys.argv) != 2:  # noqa: PLR2004
        print("Usage: google_auth_decoder <url>")  # noqa: T201
        sys.exit(1)

    url = sys.argv[1]
    result = decode_url(url)

    for item in result:
        print(item)  # noqa: T201


if __name__ == "__main__":
    main()
