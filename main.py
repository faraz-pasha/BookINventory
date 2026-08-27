import sys

from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow

from database import initialize_database
from app_paths import resource_path


initialize_database()


app = QApplication(
    sys.argv
)


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


window = MainWindow()

window.show()


sys.exit(
    app.exec()
)