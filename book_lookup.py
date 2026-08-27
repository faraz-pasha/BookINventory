import json
import urllib.parse
import urllib.request
from app_paths import IMAGES_DIR
from uuid import uuid4
from urllib.error import HTTPError


SHELFIE_API_URL = (
    "https://shelfie-api-vclz.onrender.com"
)


def search_books(
    title,
    author="",
    max_results=10
):

    title = title.strip()
    author = author.strip()

    if not title:
        return []

    parameters = {
        "title":
            title,

        "author":
            author,

        "max_results":
            max_results,
    }

    url = (
        SHELFIE_API_URL
        + "/books/search?"
        + urllib.parse.urlencode(
            parameters
        )
    )

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent":
                "Shelfie"
        }
    )

    try:

        with urllib.request.urlopen(
            request,
            timeout=30
        ) as response:

            data = json.load(
                response
            )


    except HTTPError as error:

        error_body = (

            error.read()

            .decode(

                "utf-8",

                errors="replace"

            )

        )

        try:

            error_data = json.loads(

                error_body

            )

            detail = error_data.get(

                "detail",

                error_body

            )


        except Exception:

            detail = error_body

        raise RuntimeError(

            (

                f"Shelfie API returned HTTP "

                f"{error.code}.\n\n"

                f"{detail}"

            )

        ) from error
    
    except Exception as error:

        raise RuntimeError(
            "Could not connect to the Shelfie service.\n\n"
            f"{error}"
        ) from error

    return data

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