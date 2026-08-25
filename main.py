import sys

from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow

from database import initialize_database


initialize_database()


app = QApplication(sys.argv)


with open("style.qss", "r") as file:

    app.setStyleSheet(
        file.read()
    )


window = MainWindow()

window.show()


sys.exit(
    app.exec()
)