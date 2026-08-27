import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow

from database import initialize_database

from app_metadata import (
    APP_NAME,
    APP_VERSION,
    APP_ORGANIZATION,
)

from app_paths import resource_path


initialize_database()


app = QApplication(
    sys.argv
)

app.setApplicationName(
    APP_NAME
)

app.setApplicationVersion(
    APP_VERSION
)

app.setOrganizationName(
    APP_ORGANIZATION
)


# ============================================================
# Application icon
# ============================================================

icon_path = resource_path(
    "assets/icon.png"
)

if icon_path.exists():

    app.setWindowIcon(
        QIcon(
            str(icon_path)
        )
    )


# ============================================================
# Stylesheet
# ============================================================

style_path = resource_path(
    "style.qss"
)

with open(
    style_path,
    "r",
    encoding="utf-8",
) as file:

    app.setStyleSheet(
        file.read()
    )


# ============================================================
# Main window
# ============================================================

window = MainWindow()

window.show()


sys.exit(
    app.exec()
)