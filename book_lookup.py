import html
import json
import os
import time
import urllib.parse
import urllib.request
from app_paths import IMAGES_DIR
from uuid import uuid4
from urllib.error import HTTPError


GOOGLE_BOOKS_URL = (
    "https://www.googleapis.com/books/v1/volumes"
)

GOOGLE_BOOKS_API_KEY = os.getenv(
    "GOOGLE_BOOKS_API_KEY"
)


def clean_description(
    description
):

    if not description:
        return ""

    return html.unescape(
        description
    )


def get_isbn(
    industry_identifiers
):

    isbn_10 = ""
    isbn_13 = ""

    for identifier in industry_identifiers:

        identifier_type = identifier.get(
            "type"
        )

        value = identifier.get(
            "identifier",
            ""
        )

        if identifier_type == "ISBN_13":

            isbn_13 = value

        elif identifier_type == "ISBN_10":

            isbn_10 = value

    return (
        isbn_13
        or isbn_10
    )


def normalize_book(
    item
):

    volume_info = item.get(
        "volumeInfo",
        {}
    )

    authors = volume_info.get(
        "authors",
        []
    )

    categories = volume_info.get(
        "categories",
        []
    )

    image_links = volume_info.get(
        "imageLinks",
        {}
    )

    return {

        "google_books_id":
            item.get(
                "id",
                ""
            ),

        "title":
            volume_info.get(
                "title",
                ""
            ),

        "author":
            ", ".join(
                authors
            ),

        "genre":
            (
                categories[0]
                if categories
                else ""
            ),

        "pages":
            volume_info.get(
                "pageCount",
                0
            ),

        "isbn":
            get_isbn(
                volume_info.get(
                    "industryIdentifiers",
                    []
                )
            ),

        "description":
            clean_description(
                volume_info.get(
                    "description",
                    ""
                )
            ),

        "published_date":
            volume_info.get(
                "publishedDate",
                ""
            ),

        "cover_url":
            (
                image_links.get(
                    "thumbnail"
                )
                or image_links.get(
                    "smallThumbnail"
                )
                or ""
            ),
    }


def search_books(
    title,
    author="",
    max_results=10
):

    if not GOOGLE_BOOKS_API_KEY:

        raise RuntimeError(
            "Google Books API key is not configured."
        )

    title = title.strip()
    author = author.strip()

    if not title:
        return []

    query_parts = [
        f'intitle:"{title}"'
    ]

    if author:
        query_parts.append(
            f'inauthor:"{author}"'
        )

    query = " ".join(
        query_parts
    )

    parameters = {

        "q":
            query,

        "printType":
            "books",

        "orderBy":
            "relevance",

        "maxResults":
            max_results,

        "key":
            GOOGLE_BOOKS_API_KEY,
    }

    url = (
        GOOGLE_BOOKS_URL
        + "?"
        + urllib.parse.urlencode(
            parameters
        )
    )

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent":
                "BookInventory"
        }
    )

    data = None

    # --------------------------------------------------------
    # Google request with retry
    # --------------------------------------------------------

    for attempt in range(
        3
    ):

        try:

            with urllib.request.urlopen(
                request,
                timeout=10
            ) as response:

                data = json.load(
                    response
                )

            break

        except HTTPError as error:

            # ------------------------------------------------
            # Temporary Google Books backend failure
            # ------------------------------------------------

            if (
                error.code == 503
                and attempt < 2
            ):

                time.sleep(
                    2 ** attempt
                )

                continue

            error_body = (
                error.read()
                .decode(
                    "utf-8"
                )
            )

            raise RuntimeError(
                "Google Books lookup failed:\n\n"
                f"{error_body}"
            ) from error

        except Exception as error:

            raise RuntimeError(
                "Google Books lookup failed:\n\n"
                f"{error}"
            ) from error

    if data is None:

        raise RuntimeError(
            "Google Books lookup failed after multiple attempts."
        )

    items = data.get(
        "items",
        []
    )

    return [
        normalize_book(
            item
        )
        for item in items
    ]

def download_cover(
    cover_url
):

    if not cover_url:
        return ""

    if cover_url.startswith(
        "http://"
    ):
        cover_url = (
            "https://"
            + cover_url[
                len("http://"):
            ]
        )

    destination = (
        IMAGES_DIR
        / f"{uuid4().hex}.jpg"
    )

    request = urllib.request.Request(
        cover_url,
        headers={
            "User-Agent":
                "BookInventory"
        }
    )

    try:

        with urllib.request.urlopen(
            request,
            timeout=10
        ) as response:

            destination.write_bytes(
                response.read()
            )

    except Exception as error:

        raise RuntimeError(
            f"Cover download failed: {error}"
        ) from error

    return str(
        destination
    )