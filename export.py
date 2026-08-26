import csv
from pathlib import Path


def export_library(destination_file, books):

    destination_file = Path(
        destination_file
    )

    if destination_file.suffix.lower() != ".csv":
        destination_file = destination_file.with_suffix(
            ".csv"
        )

    if not books:
        raise ValueError(
            "There are no books to export."
        )

    fieldnames = [
        key
        for key in books[0].keys()
        if key != "cover"
    ]

    with destination_file.open(
        "w",
        newline="",
        encoding="utf-8-sig",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()

        for book in books:
            row = {
                key: value
                for key, value in book.items()
                if key != "cover"
            }

            writer.writerow(
                row
            )

    return destination_file