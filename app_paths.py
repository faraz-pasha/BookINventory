import shutil
import sqlite3
import sys
from pathlib import Path


APP_NAME = "BookInventory"

PROJECT_ROOT = Path(
    __file__
).resolve().parent


# ============================================================
# Application data directory
# ============================================================

def get_data_dir():

    if sys.platform == "darwin":

        base_dir = (
            Path.home()
            / "Library"
            / "Application Support"
        )

    elif sys.platform == "win32":

        base_dir = (
            Path.home()
            / "AppData"
            / "Local"
        )

    else:

        base_dir = (
            Path.home()
            / ".local"
            / "share"
        )

    data_dir = (
        base_dir
        / APP_NAME
    )

    data_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    return data_dir


DATA_DIR = get_data_dir()


# ============================================================
# Database
# ============================================================

DATABASE_DIR = (
    DATA_DIR
    / "database"
)

DATABASE_DIR.mkdir(
    parents=True,
    exist_ok=True
)

DB_PATH = (
    DATABASE_DIR
    / "library.db"
)


# ============================================================
# Cover images
# ============================================================

IMAGES_DIR = (
    DATA_DIR
    / "images"
)

IMAGES_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# Legacy development paths
# ============================================================

LEGACY_DB_PATH = (
    PROJECT_ROOT
    / "database"
    / "library.db"
)

LEGACY_IMAGES_DIR = (
    PROJECT_ROOT
    / "images"
)


# ============================================================
# Legacy data migration
# ============================================================

def migrate_legacy_data():

    database_was_migrated = False

    # --------------------------------------------------------
    # Copy old database
    # --------------------------------------------------------

    if (
        not DB_PATH.exists()
        and LEGACY_DB_PATH.exists()
    ):

        shutil.copy2(
            LEGACY_DB_PATH,
            DB_PATH
        )

        database_was_migrated = True

    # --------------------------------------------------------
    # Copy old cover images
    # --------------------------------------------------------

    if LEGACY_IMAGES_DIR.exists():

        for source in LEGACY_IMAGES_DIR.iterdir():

            if not source.is_file():
                continue

            destination = (
                IMAGES_DIR
                / source.name
            )

            if not destination.exists():

                shutil.copy2(
                    source,
                    destination
                )

    # --------------------------------------------------------
    # Convert old relative cover paths
    # --------------------------------------------------------

    if (
        database_was_migrated
        and DB_PATH.exists()
    ):

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

                # Already absolute: leave it alone
                if old_path.is_absolute():
                    continue

                # Old versions normally stored:
                # images/filename.jpg
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

def resource_path(
    relative_path
):

    if getattr(
        sys,
        "frozen",
        False
    ):

        base_path = Path(
            sys._MEIPASS
        )

    else:

        base_path = PROJECT_ROOT

    return (
        base_path
        / relative_path
    )