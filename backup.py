import shutil
import tempfile
from pathlib import Path


DB_PATH = Path("database/library.db")
IMAGES_PATH = Path("images")


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

        temp_path = Path(temp_dir)

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

        if IMAGES_PATH.exists():

            shutil.copytree(
                IMAGES_PATH,
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

        temp_path = Path(temp_dir)

        # ----------------------------------------------------
        # Extract backup
        # ----------------------------------------------------

        shutil.unpack_archive(
            backup_file,
            temp_path,
            "zip",
        )

        backup_database = (
            temp_path / "library.db"
        )

        backup_images = (
            temp_path / "images"
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

        if IMAGES_PATH.exists():
            shutil.rmtree(
                IMAGES_PATH
            )

        if backup_images.exists():

            shutil.copytree(
                backup_images,
                IMAGES_PATH,
            )

        else:

            IMAGES_PATH.mkdir(
                parents=True,
                exist_ok=True,
            )