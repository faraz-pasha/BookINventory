import shutil
import sqlite3
import tempfile
from pathlib import Path

from app_paths import (
    DB_PATH,
    IMAGES_DIR,
)


def create_backup(destination_file):

    destination_file = Path(
        destination_file
    )

    # Make sure the backup has a .zip extension
    if destination_file.suffix.lower() != ".zip":

        destination_file = (
            destination_file.with_suffix(".zip")
        )

    with tempfile.TemporaryDirectory() as temp_dir:

        temp_path = Path(
            temp_dir
        )

        # ----------------------------------------------------
        # Copy database
        # ----------------------------------------------------

        if DB_PATH.exists():

            shutil.copy2(
                DB_PATH,
                temp_path / "library.db",
            )

        # ----------------------------------------------------
        # Copy cover images
        # ----------------------------------------------------

        if IMAGES_DIR.exists():

            shutil.copytree(
                IMAGES_DIR,
                temp_path / "images",
            )

        # ----------------------------------------------------
        # Create ZIP archive
        # ----------------------------------------------------

        archive_path = shutil.make_archive(
            str(
                destination_file.with_suffix("")
            ),
            "zip",
            temp_path,
        )

    return Path(
        archive_path
    )


def restore_backup(backup_file):

    backup_file = Path(
        backup_file
    )

    if not backup_file.exists():

        raise FileNotFoundError(
            "Backup file does not exist."
        )

    with tempfile.TemporaryDirectory() as temp_dir:

        temp_path = Path(
            temp_dir
        )

        # ----------------------------------------------------
        # Extract backup
        # ----------------------------------------------------

        shutil.unpack_archive(
            backup_file,
            temp_path,
            "zip",
        )

        backup_database = (
            temp_path
            / "library.db"
        )

        backup_images = (
            temp_path
            / "images"
        )

        # ----------------------------------------------------
        # Validate backup
        # ----------------------------------------------------

        if not backup_database.exists():

            raise ValueError(
                "This is not a valid Book Inventory backup."
            )

        # ----------------------------------------------------
        # Restore database
        # ----------------------------------------------------

        DB_PATH.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        shutil.copy2(
            backup_database,
            DB_PATH,
        )

        # ----------------------------------------------------
        # Restore cover images
        # ----------------------------------------------------

        if IMAGES_DIR.exists():

            shutil.rmtree(
                IMAGES_DIR
            )

        if backup_images.exists():

            shutil.copytree(
                backup_images,
                IMAGES_DIR,
            )

        else:

            IMAGES_DIR.mkdir(
                parents=True,
                exist_ok=True,
            )

        # ----------------------------------------------------
        # Normalize restored cover paths
        # ----------------------------------------------------

        normalize_cover_paths()


def normalize_cover_paths():

    if not DB_PATH.exists():
        return

    conn = sqlite3.connect(
        DB_PATH
    )

    try:

        rows = conn.execute(
            """
            SELECT id, cover
            FROM books
            WHERE cover IS NOT NULL
              AND cover != ''
            """
        ).fetchall()

        for book_id, cover_path in rows:

            old_path = Path(
                cover_path
            )

            filename = old_path.name

            new_path = (
                IMAGES_DIR
                / filename
            )

            if new_path.exists():

                conn.execute(
                    """
                    UPDATE books
                    SET cover = ?
                    WHERE id = ?
                    """,
                    (
                        str(new_path),
                        book_id,
                    )
                )

        conn.commit()

    finally:

        conn.close()